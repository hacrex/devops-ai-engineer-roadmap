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
