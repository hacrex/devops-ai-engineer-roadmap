# ☸️ Kubernetes AI: vLLM, KServe, Ray & Autoscaling at Scale

Running single-instance local models is excellent for testing, but hosting enterprise-scale GenAI requires a cloud-native, auto-scaling, high-availability cluster architecture. A DevOps AI Engineer must master scheduling physical hardware, orchestrating serving engines (like **vLLM** and **KServe**), slicing GPUs via **MIG (Multi-Instance GPU)**, and configuring event-driven autoscaling using **KEDA**.

---

## 🏗️ Enterprise Production Inference Architecture

```
                                ┌────────────────────────┐
                                │   Istio Ingress Gateway│
                                └───────────┬────────────┘
                                            │ HTTP (JWT Auth)
                                            ▼
                                ┌────────────────────────┐
                                │   KServe Controller    │
                                └───────────┬────────────┘
                                            │ Configures
                                            ▼
                    ┌────────────────────────────────────────┐
                    │      Kubernetes Pod Autoscaling        │
                    │   ┌──────────────┐  ┌──────────────┐   │
                    │   │ vLLM Pod 1   │  │ vLLM Pod 2   │   │
                    │   │ - GPU Core 0 │  │ - GPU Core 1 │   │
                    │   └──────┬───────┘  └──────┬───────┘   │
                    └──────────┼─────────────────┼───────────┘
                               │ Prom Metrics    │
                               ▼                 ▼
                        ┌──────────────────────────────┐
                        │     Prometheus Monitor       │
                        └──────────────┬───────────────┘
                                       │ Scrapes Queue length
                                       ▼
                        ┌──────────────────────────────┐
                        │      KEDA Autoscaler         │
                        │   Scales Pod replicas up/dn  │
                        └──────────────────────────────┘
```

---

## 📘 Advanced Cluster AI Concepts

### 1. NVIDIA GPU Operator & Device Plugin
Standard Kubernetes has no native knowledge of graphics cards. The **NVIDIA GPU Operator** uses Kubernetes operators to automatically provision the required host-level NVIDIA drivers, container runtimes, monitoring exporters, and the device plugin.
* The plugin labels nodes with available graphics capabilities and exposes `nvidia.com/gpu` as a schedulable resource pool.

### 2. Multi-Instance GPU (MIG) vs. Time-Slicing
* **Time-Slicing**: Standard GPU virtualization where multiple containers share execution *time* on the same GPU. The downside is that memory space is shared; if one pod crashes or leaks, all pods sharing that GPU fail.
* **MIG (Multi-Instance GPU)**: Physically partitions a single massive GPU (like an A100 or H100) into up to 7 fully isolated hardware instances. Each instance has its own dedicated memory (vRAM) and processing cores, providing absolute hardware isolation and guaranteed quality of service (QoS).

### 3. vLLM Engine & PagedAttention
Serving models via raw Python processes is highly inefficient. **vLLM** is a high-throughput, low-latency LLM serving engine.
* **PagedAttention**: Rather than pre-allocating contiguous memory blocks for virtual prompt keys/values (KV cache)—which wastes up to 60-80% of vRAM—PagedAttention divides the KV cache into logical blocks. This allows vLLM to scale concurrent serving capacity by up to 24x with zero memory fragmentation.

---

## 🛠️ Hands-on Lab: High-Availability vLLM Deployment on Kubernetes

In this lab, you will write and deploy a complete production-grade Kubernetes manifest hosting vLLM with high-availability configurations, custom readiness/liveness probes, and an automated KEDA queue scaler.

### Step 1: Create a High-Availability Deployment
Create `vllm-deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vllm-llama-serving
  namespace: ai-platform
  labels:
    app: vllm-engine
spec:
  replicas: 2
  selector:
    matchLabels:
      app: vllm-engine
  template:
    metadata:
      labels:
        app: vllm-engine
    spec:
      # Ensure pods are scheduled across different nodes to maintain high availability
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - vllm-engine
              topologyKey: kubernetes.io/hostname
      
      # Taint toleration: Schedule only on nodes labeled with GPU hardware
      tolerations:
      - key: "sku"
        operator: "Equal"
        value: "gpu"
        effect: "NoSchedule"

      containers:
      - name: vllm-container
        image: vllm/vllm-openai:v0.3.2
        args:
          - "--model"
          - "meta-llama/Meta-Llama-3-8B-Instruct"
          - "--port"
          - "8000"
          - "--gpu-memory-utilization"
          - "0.90" # Reserve 90% VRAM for model and KV Cache
          - "--max-model-len"
          - "4096"
        env:
          - name: HUGGING_FACE_HUB_TOKEN
            valueFrom:
              secretKeyRef:
                name: hf-secret
                key: token
        ports:
        - containerPort: 8000
          name: http
        resources:
          requests:
            cpu: "4"
            memory: "16Gi"
            nvidia.com/gpu: "1"
          limits:
            cpu: "8"
            memory: "32Gi"
            nvidia.com/gpu: "1"
        
        # Probes specifically tuned for LLM cold startups (Loading weights takes time!)
        startupProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 15
          failureThreshold: 20 # Wait up to 5 minutes for large weight downloads
          
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          periodSeconds: 10
          
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          periodSeconds: 30
```

### Step 2: Create Ingress and Service Definitions
Create `vllm-service.yaml`:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: vllm-service
  namespace: ai-platform
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "8000"
spec:
  type: ClusterIP
  ports:
  - port: 80
    targetPort: 8000
    protocol: TCP
    name: http
  selector:
    app: vllm-engine
```

### Step 3: Implement Queue-Based Autoscaling using KEDA
Standard CPU/RAM horizontal pod autoscalers (HPA) fail on AI workloads because running model matrix calculations uses 100% compute resources instantly, causing premature scaling loops. KEDA dynamically scales replicas up or down based on the number of waiting requests in the vLLM scheduler queue.

Create `keda-scaler.yaml`:
```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: vllm-keda-scaler
  namespace: ai-platform
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: vllm-llama-serving
  minReplicaCount: 1
  maxReplicaCount: 5
  cooldownPeriod: 300 # Wait 5 minutes before scaling down to prevent flapping
  triggers:
  - type: prometheus
    metadata:
      serverAddress: http://prometheus-k8s.monitoring.svc:9090
      metricName: vllm_num_requests_waiting
      # Trigger scale up if the waiting request queue exceeds 5
      query: sum(vllm:num_requests_waiting)
      threshold: '5'
```

---

## 🔒 Security Considerations
1. **Model Theft Prevention**: Restrict local execution pods from running arbitrary debugging shells (`exec`). Block unauthorized container root privileges using securityContext parameters.
2. **Cluster egress policies**: Ensure the namespace housing LLM workloads blocks outgoing internet routing unless explicitly authenticated to secure weight providers (like HuggingFace/S3).
3. **Data isolation**: Enforce dedicated node pools for AI, physically segregating tenant client workloads from general business microservices.

---

## 📈 Scaling & Observability Considerations
* **Cold Starts**: Implement Model Cache Pre-Warming using DaemonSets to cache `.safetensors` weight directories directly onto host NVMe folders.
* **Metric Scraping**: Query custom vLLM Prometheus metrics:
  * `vllm:num_requests_waiting` (Scheduler queue density - core scaling driver).
  * `vllm:gpu_cache_usage_factor` (VRAM KV-cache consumption rate).

---

## 🔍 Troubleshooting Guide

### 💥 Issue: Pod Fails Startup Probes and Restarts in a Loop (`CrashLoopBackOff`)
* **Root Cause**: The startup probes are timed out or fail before the massive model weight layers are loaded from disk into memory.
* **Mitigation**:
  1. Increase the `failureThreshold` parameter in the `startupProbe` definition.
  2. Implement an InitContainer to handle the initial HuggingFace weight downloads, keeping serving startup routines completely separate.
  3. Ensure network bandwidth limits are not throttling S3 download threads.

---

## 🌟 Best Practices & Open-Source Tools
* **KServe**: A model-agnostic serving orchestration tool offering virtual auto-wrapping, zero-downtime Canary rollouts, and multi-tenant isolation.
* **KEDA**: Event-driven autoscaling provider to orchestrate scale-up/scale-down rules using PromQL or Message Queue length.
