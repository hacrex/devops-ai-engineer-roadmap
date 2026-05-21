# 🐳 Containerization, OCI Runtimes & Multi-Stage GPU Dockerfiles

Running standard web microservices in Docker is simple. Running AI workloads requires container runtimes to interface directly with physical GPU hardware. A DevOps AI Engineer must master OCI runtimes, configure host-level GPU pass-through container runtimes (`nvidia-container-runtime`), and build highly optimized Dockerfiles to shrink deep learning container images from 15GB+ monstrosities down to slim, fast-starting footprints.

---

## 🏗️ Container Runtime Architecture with GPU Pass-Through

```
┌────────────────────────────────────────────────────────────────────────┐
│ USER SPACE (Container Lifecycle)                                       │
│ Docker CLI / Kubernetes Kubelet                                        │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼ Container Spec (config.json)
┌────────────────────────────────────────────────────────────────────────┐
│ CONTAINER RUNTIME (High-Level)                                         │
│ containerd / CRI-O                                                     │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ OCI RUNTIME (Low-Level) & GPU DRIVER PASS-THROUGH                      │
│ - runc (standard CPU execution)                                        │
│ - nvidia-container-runtime (Injects host GPU libraries & dev nodes)    │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ PHYSICAL SYSTEM                                                        │
│ Host Kernel (cgroups v2) ──► Host NVIDIA Drivers ──► Host GPUs (L4/A100)│
└────────────────────────────────────────────────────────────────────────┘
```

---

## 📘 Core Containerization Concepts for AI

### 1. NVIDIA Container Toolkit & Runtime
Standard container environments isolate the container filesystem and process tree completely from host hardware. To enable a container to access the physical GPU:
* The **NVIDIA Container Toolkit** configures containerd/Docker to use `nvidia-container-runtime` as the low-level execution engine.
* When a container starts with the GPU environment variable `NVIDIA_VISIBLE_DEVICES=all`, the runtime dynamically mounts the host's CUDA driver libraries (`.so` files) and GPU device nodes (`/dev/nvidia*`) directly into the container namespace.

### 2. Multi-Stage Builds for GPU Workloads
AI applications (like PyTorch and vLLM) require complex compiler toolchains (`gcc`, `nvcc`, Python headers) to compile custom C++/CUDA kernels during build time.
* **Bad Practice**: Bundling full compilers inside the final container image (leads to 15GB+ images, slow deployment times, and massive security attack surfaces).
* **Multi-Stage Solution**: Use a heavy developer image (e.g., `cuda:xx.x-devel`) to compile the virtual environment and wheel packages, and copy *only* the compiled artifacts and runtime dependencies into a clean, lightweight runner base image (e.g., `cuda:xx.x-runtime`).

---

## 🛠️ Hands-on Containerization Lab

In this lab, you will configure your Docker daemon to support GPUs, write a highly optimized multi-stage Python/PyTorch Dockerfile, and run it using Docker Compose with GPU resource allocation.

### Step 1: Configure Docker Daemon for NVIDIA Container Runtime
Edit `/etc/docker/daemon.json` (on Linux host with NVIDIA GPU installed) to configure the runtime:
```json
{
  "runtimes": {
    "nvidia": {
      "path": "nvidia-container-runtime",
      "runtimeArgs": []
    }
  },
  "default-runtime": "nvidia"
}
```
Restart docker: `sudo systemctl restart docker`.

### Step 2: Write an Optimized Multi-Stage Dockerfile
Create a `Dockerfile` for an inference API application:
```dockerfile
# ==========================================
# STAGE 1: Builder (Heavy Compilers included)
# ==========================================
FROM nvidia/cuda:12.1.1-devel-ubuntu22.04 AS builder

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies needed for compiling python extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-dev \
    python3-pip \
    python3-venv \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set up virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install deep learning wheels (PyTorch with exact CUDA 12.1 support)
RUN pip3 install --no-cache-dir --upgrade pip setuptools wheel && \
    pip3 install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Install fastapi for serving
RUN pip3 install --no-cache-dir fastapi uvicorn pydantic

# ==========================================
# STAGE 2: Runtime Runner (Slim production image)
# ==========================================
FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04 AS runner

# Set non-interactive and environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    NVIDIA_DRIVER_CAPABILITIES=compute,utility

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-distutils \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy compiled virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# Create a non-root system user for security
RUN useradd -u 1000 -m aiuser
USER aiuser

# Create workspace directory
WORKDIR /home/aiuser/app

# Copy application source code
COPY --chown=aiuser:aiuser src/ .

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Step 3: Launch with Docker Compose and GPU Resource Reservation
Create a `docker-compose.yml` to run the optimized container:
```yaml
version: '3.8'

services:
  inference-api:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
      - MODEL_NAME=Qwen/Qwen2.5-Coder-7B-Instruct
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    restart: unless-stopped
```

To run this cluster setup:
```bash
docker-compose up -d --build
```

---

## ⚡ Production Kubernetes Pod GPU Manifest

To consume the container image compiled in the lab inside a Kubernetes cluster, we mount the host GPU device explicitly using scheduling resource allocations:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: gpu-inference-pod
  namespace: ai-platform
  labels:
    app: vllm-inference
spec:
  containers:
  - name: engine
    image: my-private-registry/ai/inference-engine:latest
    ports:
    - containerPort: 8000
    resources:
      limits:
        cpu: "4"
        memory: 16Gi
        nvidia.com/gpu: "1" # Explicitly requests 1 NVIDIA GPU from cluster pool
      requests:
        cpu: "2"
        memory: 8Gi
        nvidia.com/gpu: "1"
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      runAsNonRoot: true
      runAsUser: 1000
```

---

## 🔒 Security Considerations
1. **ReadOnly Filesystem**: Configure containers with `readOnlyRootFilesystem: true`. Write temp cache parameters or model weights exclusively to dedicated directories mounted on fast external storage (`/tmp` or Persistent Volumes).
2. **Base Image Trust**: Only consume official base images directly from official vendor accounts (such as `nvidia/cuda` on DockerHub) to avoid supply-chain poisoning.
3. **Scan Vulnerabilities**: Integrate `trivy` or `aquasec` into the container CI/CD pipeline to flag outdated CUDA or OS system library components before pushing to registries.

---

## 📈 Scaling & Observability Considerations
* **Layer Caching**: Structure your Dockerfile commands so that lines that rarely change (`apt install`, `pip install PyTorch`) sit at the top. This maximizes layer reuse and dramatically reduces build speeds from 25 minutes to under 30 seconds when application files change.
* **Cgroup Constraints**: Avoid scaling container limits blindly. CPU-bound inference scripts should utilize thread locking to prevent processes from bouncing across CPU nodes, which causes cache degradation.

---

## 🔍 Troubleshooting Guide

### 💥 Issue: `docker: Error response from daemon: could not select device driver "" with capabilities: [[gpu]]`
* **Root Cause**: The host system lacks the **NVIDIA Container Toolkit** or Docker is not configured to utilize the custom `nvidia` container runtime.
* **Diagnostic Command**:
  ```bash
  # Check if nvidia container runtime is registered
  docker info | grep -i runtime
  ```
* **Mitigation**:
  1. Install the toolkit on the host: `sudo apt-get install -y nvidia-container-toolkit`.
  2. Generate configuration bindings: `sudo nvidia-ctk runtime configure --runtime=docker`.
  3. Restart the Docker daemon: `sudo systemctl restart docker`.

---

## 🌟 Best Practices & Open-Source Tools
* **Trivy**: Run static container analysis: `trivy image my-inference-image:latest` to identify security loopholes.
* **Dive**: Utilize `dive` to inspect container layers, identify duplicate files, and locate wasted space in your built Docker images.
