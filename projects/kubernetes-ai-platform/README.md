# 📁 Project 4: Production-Grade Kubernetes AI Inference Platform

This project is a complete, enterprise-ready blueprint for a **Kubernetes AI Inference Platform**. It details how to provision GPU-enabled Kubernetes clusters programmatically using Terraform, deploy high-throughput models via **vLLM** wrapped inside **KServe InferenceServices**, and orchestrate dynamic queue-length autoscaling using **KEDA**.

---

## 🏗️ Platform Cluster Topology

```
                                ┌────────────────────────┐
                                │ Istio Ingress Gateway  │
                                └───────────┬────────────┘
                                            │ JWT / API Authorization
                                            ▼
                                ┌────────────────────────┐
                                │   KServe Controller    │
                                └───────────┬────────────┘
                                            │ Configures
                                            ▼
                    ┌────────────────────────────────────────┐
                    │      GKE Dedicated GPU Node Pools      │
                    │   ┌──────────────┐  ┌──────────────┐   │
                    │   │ vLLM Pod 1   │  │ vLLM Pod 2   │   │
                    │   │ - NVIDIA L4  │  │ - NVIDIA L4  │   │
                    │   └──────┬───────┘  └──────┬───────┘   │
                    └──────────┼─────────────────┼───────────┘
                               │ Metrics Exporter│
                               ▼                 ▼
                        ┌──────────────────────────────┐
                        │      Prometheus Server       │
                        └──────────────┬───────────────┘
                                       │ Scrapes Queue metrics
                                       ▼
                        ┌──────────────────────────────┐
                        │    KEDA Autoscaling Engine   │
                        └──────────────────────────────┘
```

---

## 🏗️ Terraform Infrastructure Provisioning (Google Cloud GKE)

This module provisions a highly available Google Kubernetes Engine (GKE) cluster containing an isolated private network, a standard CPU node pool for administration, and a highly scalable, dedicated GPU node pool pre-configured for NVIDIA L4 accelerators.

### 1. Main Configuration (`terraform-gke-gpu/main.tf`)
```hcl
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# 1. Dedicated VPC for AI Workloads
resource "google_compute_network" "ai_vpc" {
  name                    = "ai-platform-vpc"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "ai_subnet" {
  name          = "ai-platform-subnet"
  ip_cidr_range = "10.150.0.0/20"
  region        = var.region
  network       = google_compute_network.ai_vpc.id
}

# 2. Main GKE Cluster
resource "google_container_cluster" "ai_cluster" {
  name     = "ai-production-cluster"
  location = "${var.region}-a"

  network    = google_compute_network.ai_vpc.name
  subnetwork = google_compute_subnetwork.ai_subnet.name

  # Enable IP-Aliasing for container native routing
  ip_allocation_policy {
    cluster_ipv4_cidr_block  = "/14"
    services_ipv4_cidr_block = "/20"
  }

  # Deploy minimal default node pool (to be immediately replaced)
  remove_default_node_pool = true
  initial_node_count       = 1
}

# 3. System Node Pool (Standard administrative tasks)
resource "google_container_node_pool" "system_nodes" {
  name       = "system-node-pool"
  location   = google_container_cluster.ai_cluster.location
  cluster    = google_container_cluster.ai_cluster.name
  node_count = 2

  node_config {
    machine_type = "e2-standard-4"
    oauth_scopes = ["https://www.googleapis.com/auth/cloud-platform"]
  }
}

# 4. GPU-Accelerated Node Pool (vLLM Model execution)
resource "google_container_node_pool" "gpu_nodes" {
  name       = "nvidia-gpu-pool"
  location   = google_container_cluster.ai_cluster.location
  cluster    = google_container_cluster.ai_cluster.name
  node_count = 1

  autoscaling {
    min_node_count = 1
    max_node_count = 5
  }

  node_config {
    machine_type = "g2-standard-8" # 8 vCPUs, 32GB RAM

    guest_accelerator {
      type  = "nvidia-l4"
      count = 1
    }

    # Schedulers require taints to prevent standard pods from polluting GPU RAM
    taint {
      key    = "sku"
      value  = "gpu"
      effect = "NO_SCHEDULE"
    }

    labels = {
      "hardware-type"  = "gpu"
      "nvidia.com/gpu" = "present"
    }

    oauth_scopes = ["https://www.googleapis.com/auth/cloud-platform"]
  }
}
```

### 2. Variables Configuration (`terraform-gke-gpu/variables.tf`)
```hcl
variable "project_id" {
  description = "The target Google Cloud Project ID"
  type        = string
}

variable "region" {
  description = "The GCP region to deploy E2 / GPU nodes"
  type        = string
  default     = "us-central1"
}
```

---

## ⚡ KServe InferenceService Deployment Spec

To run high-throughput LLM engines, we define a declarative KServe InferenceService that runs vLLM under the hood, mounts GPU hardware requirements, and sets standard liveness thresholds:

Create `vllm-kserve.yaml`:
```yaml
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: llama-3-8b-serving
  namespace: ai-platform
spec:
  predictor:
    model:
      modelFormat:
        name: huggingface
      resources:
        limits:
          cpu: "4"
          memory: 16Gi
          nvidia.com/gpu: "1" # Mounts physical GPU
        requests:
          cpu: "2"
          memory: 8Gi
          nvidia.com/gpu: "1"
      # Toleration for node taint mapping
      tolerations:
      - key: "sku"
        operator: "Equal"
        value: "gpu"
        effect: "NoSchedule"
      # Configure container arguments to start vLLM
      args:
        - "--model"
        - "meta-llama/Meta-Llama-3-8B-Instruct"
        - "--port"
        - "8080"
        - "--max-model-len"
        - "4096"
```

---

## ⚡ KEDA Event-Driven Scale Spec

Configure KEDA to scale the running KServe inference pod instances dynamically from 1 to 5 based on the active Prometheus query measuring the pending request queue:

Create `keda-scaler.yaml`:
```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: vllm-keda-autoscaler
  namespace: ai-platform
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: llama-3-8b-serving-predictor-default
  minReplicaCount: 1
  maxReplicaCount: 5
  cooldownPeriod: 300 # Cooldown wait buffer to avoid pod flapping
  triggers:
  - type: prometheus
    metadata:
      serverAddress: http://prometheus-k8s.monitoring.svc:9090
      metricName: vllm_num_requests_waiting
      # Target query sum
      query: sum(vllm:num_requests_waiting)
      threshold: '5'
```

---

## 🚀 Step-by-Step Platform Setup

### 1. Provision Infrastructure via Terraform
```bash
cd terraform-gke-gpu
terraform init
terraform plan -var="project_id=my-gcp-project"
# terraform apply -var="project_id=my-gcp-project" -auto-approve
```

### 2. Configure NVIDIA GPU Drivers
Once GKE is active, configure Google's official daemon extension to auto-load host NVIDIA drivers:
```bash
kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/container-engine-accelerators/master/nvidia-driver-installer/cos/daemonset-preloaded-latest.yaml
```

### 3. Deploy Platform Resources
Apply the serving and scaling manifests to complete the setup:
```bash
kubectl create namespace ai-platform
kubectl apply -f vllm-kserve.yaml
kubectl apply -f keda-scaler.yaml
```
Your high-performance, auto-scaling model serving portal is now fully functional!
```bash
kubectl get inferenceservice -n ai-platform
```
