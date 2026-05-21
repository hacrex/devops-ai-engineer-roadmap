# ☸️ Kubernetes Basics, Pod Lifecycles & Helm Charts for AI Workloads

For modern enterprise AI, Kubernetes is the standard operating system. It orchestrates high-performance model deployments across dozens of multi-GPU nodes, manages high-throughput networking, abstracts block storage, and scales resources dynamically based on demand. A DevOps AI Engineer must master core Kubernetes components, pod lifecycles, configuration injection, and deployment packaging using Helm.

---

## 🏗️ Kubernetes Cluster Architecture for AI Runtimes

```
┌────────────────────────────────────────────────────────────────────────┐
│ CONTROL PLANE (Management & Scheduling)                                │
│ API Server ◄─── etcd (State) ◄─── Controller Manager ◄─── Scheduler    │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Orchestrates
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ DATA PLANE (Worker Nodes)                                              │
│  ┌─────────────────────────────┐      ┌─────────────────────────────┐  │
│  │ GPU WORKER NODE 1           │      │ GPU WORKER NODE 2           │  │
│  │ - Kubelet      - Kube-Proxy │      │ - Kubelet      - Kube-Proxy │  │
│  │ - NVIDIA GPU  - Pod (vLLM)  │      │ - NVIDIA GPU  - Pod (vLLM)  │  │
│  └─────────────────────────────┘      └─────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 📘 Essential Kubernetes Concepts

### 1. Pod Lifecycle & InitContainers
A Pod is the smallest deployable unit in Kubernetes. In AI setups, Pod lifecycles often feature an **InitContainer** to execute initial preparation before the core serving engine (e.g. PyTorch, vLLM) starts up.
* **InitContainer Role**: Pull heavy model files from a remote repository (Hugging Face, AWS S3) and store them in a local NVMe cache directory.
* **Core Container Role**: Read cached weights from local disk, load them into GPU vRAM, and start the inference server.

### 2. ConfigMaps and Secrets
* **ConfigMaps**: Store non-sensitive parameters (e.g., model hyperparameters, prompt templates, backend API URLs).
* **Secrets**: Encrypt and store sensitive values (e.g., Hugging Face access tokens, database connection keys). These are mounted into pods as files or environment variables.

### 3. Helm Charts
Helm is the package manager for Kubernetes. Instead of managing dozens of isolated YAML templates, Helm uses parameterized templates (`values.yaml`) to standardize deployments across Dev, Staging, and Production environments.

---

## 🛠️ Hands-on Deployment Lab: Python AI Microservice

In this lab, you will deploy a multi-resource application cluster containing a ConfigMap, a Secret, a Deployment featuring an InitContainer, and a ClusterIP Service.

### Step 1: Create ConfigMap and Secret manifests
Create `config-secret.yaml`:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: ai-model-config
  namespace: default
data:
  MODEL_NAME: "Qwen/Qwen2.5-0.5B-Instruct"
  TEMPERATURE: "0.7"
  MAX_TOKENS: "512"

---
apiVersion: v1
kind: Secret
metadata:
  name: ai-model-secret
  namespace: default
type: Opaque
stringData:
  HF_TOKEN: "hf_abc123thisismytokensecret"
```

### Step 2: Create a Pod Deployment with an InitContainer
Create `deployment.yaml`. The InitContainer downloads files to a shared volume, and the core app consumes them:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-inference-deployment
  namespace: default
  labels:
    app: ai-inference
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ai-inference
  template:
    metadata:
      labels:
        app: ai-inference
    spec:
      # Shared high-speed memory volume
      volumes:
      - name: model-cache-volume
        emptyDir: {}

      # InitContainer downloads model weights
      initContainers:
      - name: weight-downloader
        image: alpine:3.18
        command: ["sh", "-c"]
        args:
          - |
            echo "Starting model weights pull..."
            # Simulate downloading files to model-cache-volume
            echo "Model weight binary files downloaded." > /cache/mock_model.bin
            echo "Pull finished!"
        volumeMounts:
        - name: model-cache-volume
          mountPath: /cache

      # Core Container boots inference server
      containers:
      - name: inference-engine
        image: python:3.10-slim
        command: ["python3", "-c"]
        args:
          - |
            import time
            import os
            print(f"Loading Model: {os.environ.get('MODEL_NAME')}")
            print(f"Reading downloaded weights from: /cache/mock_model.bin")
            with open('/cache/mock_model.bin', 'r') as f:
                print(f"Weights verification: {f.read().strip()}")
            print("Inference service is healthy & running!")
            while True:
                time.sleep(3600)
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: ai-model-config
        env:
        - name: HF_TOKEN
          valueFrom:
            secretKeyRef:
              name: ai-model-secret
              key: HF_TOKEN
        volumeMounts:
        - name: model-cache-volume
          mountPath: /cache
        resources:
          requests:
            cpu: "500m"
            memory: "1Gi"
          limits:
            cpu: "1"
            memory: "2Gi"
```

### Step 3: Create a Service and Ingress Gateway
Create `service.yaml`:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: ai-inference-service
  namespace: default
spec:
  type: ClusterIP
  selector:
    app: ai-inference
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
```

### Step 4: Apply and Inspect Resources
```bash
# 1. Apply all configurations to your local minikube/kind cluster
kubectl apply -f config-secret.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# 2. Monitor pod startup states
kubectl get pods -w

# 3. View container execution output
kubectl logs -f deployment/ai-inference-deployment -c inference-engine
```

---

## ⚡ Production Helm Chart Architecture

In production, orchestrate your workloads as clean Helm charts. Here is an example of a standardized structure:

```
ai-inference-chart/
├── Chart.yaml              # Chart metadata (Name, Version)
├── values.yaml             # Input configurations (ReplicaCount, Resources, Images)
└── templates/              # Kubernetes resource templates
    ├── deployment.yaml
    ├── service.yaml
    ├── ingress.yaml
    ├── configmap.yaml
    └── secret.yaml
```

### Example `values.yaml`
```yaml
replicaCount: 2

image:
  repository: my-registry/ai/inference
  tag: "1.2.0"
  pullPolicy: IfNotPresent

resources:
  requests:
    cpu: "2"
    memory: "8Gi"
    nvidia.com/gpu: "1"
  limits:
    cpu: "4"
    memory: "16Gi"
    nvidia.com/gpu: "1"

huggingFace:
  token: "hf_abc123xyz"
  modelName: "meta-llama/Llama-3-8B-Instruct"
```

---

## 🔒 Security Considerations
1. **Role-Based Access Control (RBAC)**: Enforce the Principle of Least Privilege. Runtimes must never access the Kubernetes API server root credentials. Create scoped `ServiceAccount` and `Role` definitions.
2. **Immutable ConfigMaps/Secrets**: Mark your ConfigMaps and Secrets as `immutable: true` in YAML where possible. This prevents manual accidental changes from breaking running model microservice replicas.
3. **Pod Security Standards (PSS)**: Configure Pod security policies to block root executions (`runAsNonRoot: true`), block privilege escalation, and restrict access to `/proc` and `/sys`.

---

## 📈 Scaling & Observability Considerations
* **KEDA Event Autoscaling**: Traditional metrics (CPU/RAM) are terrible indicators for scaling AI inference. Running model matrix calculations uses 100% CPU/GPU instantly, causing premature scaling loops. 
  * **Solution**: Use **KEDA** (Kubernetes Event-driven Autoscaling) to scale pods based on HTTP queue lengths or inference wait-time queues from metrics endpoints (e.g. Prometheus/vLLM endpoints).
* **State Metrics**: Collect node state parameters (`kube-state-metrics`) to track scheduling shortages and pending pod states.

---

## 🔍 Troubleshooting Guide

### 💥 Issue: Pod is Stuck in `Pending` state with "0/3 nodes are available: insufficient nvidia.com/gpu"
* **Root Cause**: The scheduler cannot find nodes in the cluster with an available physical GPU. Either the GPUs are fully consumed, or the NVIDIA Device Plugin is broken.
* **Diagnostic Command**:
  ```bash
  # View scheduling details and event queues
  kubectl describe pod <pod-name>
  ```
* **Mitigation**:
  1. Check if the cluster has autoscaling enabled on GPU nodepools (e.g., GKE autoscaler, Karpenter).
  2. Verify that the NVIDIA GPU Operator/Device Plugin is running on the worker nodes:
     ```bash
     kubectl get pods -n gpu-operator
     ```
  3. Reduce model resource requirements or implement GPU sharing (fractional GPUs) if running light workloads.

---

## 🌟 Best Practices & Open-Source Tools
* **K9s**: Use the terminal-based `k9s` interface to monitor pods, view logs, restart deployments, and inspect Kubernetes resources interactively.
* **Karpenter**: Deploy Karpenter as a node lifecycle scheduler. It provisions extremely fast, right-sized GPU virtual machines in AWS within seconds to satisfy pending Pod requirements.
