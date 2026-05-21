# 🏠 Running Local LLMs, Quantization & GPU/vRAM Sizing

For enterprise environments, sending proprietary source code, system logs, and security credentials to external cloud APIs (like OpenAI or Anthropic) introduces significant compliance risks and cost volatility. The solution is **Local Inference**—hosting open-source Large Language Models (e.g., Llama-3, Qwen, Mistral) on local workstations, private cloud VMs, or dedicated Kubernetes clusters.

---

## 🏗️ Local Inference Serving Stack

```
        ┌─────────────────────────────────────────────────────────────┐
        │  USER INTERFACE (OpenWebUI / Chat Interface)                │
        └──────────────────────────────┬──────────────────────────────┘
                                       │ HTTP API / REST
                                       ▼ (Port 11434 / 8080)
        ┌─────────────────────────────────────────────────────────────┐
        │  LOCAL INFERENCE RUNTIME (Ollama / llama.cpp / vLLM)        │
        └──────────────────────────────┬──────────────────────────────┘
                                       │ Memory Mapping (mmap)
                                       ▼
        ┌─────────────────────────────────────────────────────────────┐
        │  HARDWARE INTERFACE (CUDA / Metal / CPU AVX-512)            │
        │  - Loads compiled Quantized GGUF/AWQ layers into VRAM       │
        └─────────────────────────────────────────────────────────────┘
```

---

## 📘 Essential Local LLM Concepts

### 1. Hardware Math: GPU vRAM & Memory Bandwidth
The speed of text generation (Tokens per Second) is governed primarily by **Memory Bandwidth** (how fast weights can be read from memory into the processing cores).
* **CPU Inference**: Relies on system RAM. RAM bandwidth is slow (~50-100 GB/sec), limiting generation speeds to ~3-8 tokens/sec.
* **GPU Inference**: Relies on high-speed vRAM (HBM/GDDR). Bandwidth is extremely high (e.g. 1,000 GB/sec+ on an A100), enabling speeds of 50-100+ tokens/sec.

#### 🧮 How to calculate vRAM requirements for a model:
$$\text{Required vRAM (GB)} = \left( \frac{\text{Parameter Count (B)} \times \text{Precision (bits)}}{8} \right) \times 1.25$$
* *The 1.25 multiplier accounts for context memory overhead (KV Cache).*
* **Example**: Llama-3-8B in FP16 precision (16 bits): $(8 \times 16) / 8 \times 1.25 = 20\text{ GB}$. (Requires a 24GB GPU like RTX 3090/4090).
* **Example**: Llama-3-8B in 4-bit Quantized format: $(8 \times 4) / 8 \times 1.25 = 5\text{ GB}$. (Can easily run on standard consumer laptops or lightweight VMs!).

### 2. Quantization Formats
Quantization is the process of compressing floating-point weight parameters (usually FP16) to lower bit precisions (like 8-bit or 4-bit integers), drastically shrinking file size and memory footprint while retaining 95%+ of model reasoning capabilities.
* **GGUF**: Best for CPU and consumer GPU execution. Supports splitting model layers across CPU RAM and GPU vRAM.
* **AWQ / GPTQ**: Best for pure GPU serving. Highly optimized for CUDA environments, used extensively in high-concurrency production setups (vLLM).

---

## 🛠️ Hands-on Local Deployment Lab

In this lab, you will deploy a local inference environment using Docker Compose with CUDA acceleration, featuring **Ollama** and **OpenWebUI**.

### Step 1: Create the Docker Compose configuration
Create a file named `docker-compose.yml`:
```yaml
version: '3.8'

services:
  ollama:
    image: ollama/ollama:latest
    container_name: ollama-engine
    ports:
      - "11434:11434"
    volumes:
      - ollama_storage:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    restart: unless-stopped

  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: open-webui-portal
    ports:
      - "3000:8080"
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
    volumes:
      - webui_storage:/app/backend/data
    depends_on:
      - ollama
    restart: unless-stopped

volumes:
  ollama_storage:
  webui_storage:
```

### Step 2: Launch and pull a Model
Launch the stack:
```bash
docker-compose up -d
```
Pull a high-performance 7B parameter coding model to Ollama:
```bash
docker exec -it ollama-engine ollama run qwen2.5-coder:7b
```

### Step 3: Access OpenWebUI
Open your browser and navigate to `http://localhost:3000`. Create a local account and start prompting your private, hardware-accelerated code model!

---

## ⚡ Production Kubernetes Serving Manifest

Below is a Kubernetes YAML deployment configured to host Ollama with a dedicated local-path Persistent Volume cache, requesting exactly one NVIDIA GPU:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: ollama-model-pvc
  namespace: ai-platform
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 50Gi
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ollama-deployment
  namespace: ai-platform
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ollama-service
  template:
    metadata:
      labels:
        app: ollama-service
    spec:
      containers:
      - name: ollama
        image: ollama/ollama:0.1.48
        ports:
        - containerPort: 11434
        resources:
          limits:
            cpu: "4"
            memory: 16Gi
            nvidia.com/gpu: "1"
          requests:
            cpu: "2"
            memory: 8Gi
            nvidia.com/gpu: "1"
        volumeMounts:
        - name: model-storage
          mountPath: /root/.ollama
      volumes:
      - name: model-storage
        persistentVolumeClaim:
          claimName: ollama-model-pvc
```

---

## 🔒 Security Considerations
1. **Fully Offline Execution**: Disallow external internet connections (`Egress`) for your inference pods inside your Kubernetes cluster. Ensure models are loaded strictly from inside your secure private network registry.
2. **Access Security**: Restrict port `11434` (Ollama's management API) using Network Policies. Unprotected Ollama APIs let anyone download arbitrary models or trigger unwanted executions.
3. **CORS Restrictions**: Set standard environment boundaries (`OLLAMA_ORIGINS`) to prevent malicious websites from making browser-based API queries directly to your local endpoints.

---

## 📈 Scaling & Observability Considerations
* **vRAM Fragmentation**: When querying large models concurrently, CUDA allocations can fragment, causing Out of Memory errors. Set appropriate maximum context values (`num_ctx`) to bound RAM allocations.
* **nvidia-smi Monitoring**: Export GPU parameters (vRAM, thermal states, core utilization) using `nvidia-smi` exporters or Prometheus Exporter setups to spot latency bottlenecks.

---

## 🔍 Troubleshooting Guide

### 💥 Issue: `CUDA out of memory` during execution
* **Root Cause**: The model weight sizes combined with the KV Cache (context window buffer) exceeded the physical vRAM capacity of the allocated GPU.
* **Diagnostic Check**:
  ```bash
  # Check active VRAM utilization
  nvidia-smi
  ```
* **Mitigation**:
  1. Reduce Ollama's active context size (e.g. lower `num_ctx` in the Modelfile from 8192 to 4096).
  2. Pull a more highly compressed model quantization (e.g., migrate from 8-bit to 4-bit or 3-bit GGUF).
  3. Offload a portion of model layers onto CPU RAM using llama.cpp layer configurations (`n_gpu_layers`).

---

## 🌟 Best Practices & Open-Source Tools
* **Ollama**: The gold standard for simple local serving. It provides high-level CLI management, automatic hardware detection, and a clean REST API.
* **llama.cpp**: The under-the-hood engine driving GGUF. Offers granular, highly detailed control over CPU/GPU hybrid offloads.
