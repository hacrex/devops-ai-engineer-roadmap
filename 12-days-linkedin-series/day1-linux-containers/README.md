# 📅 Day 1: Linux & Containers in AI Infrastructure

Modern Artificial Intelligence (AI) and Machine Learning (ML) workloads demand ultra-low latency, direct access to physical hardware (GPUs/TPUs), and massive memory bandwidth. Traditional hypervisor-based virtualization introduces excessive CPU/virtual-RAM translation overhead and abstract layers that slow down weights loading. This guide covers how **Linux kernel features** and **container runtimes** form the foundation of high-performance AI infrastructure.

---

## 🏗️ Docker & Container Runtime Architecture

```
 ┌────────────────────────────────────────────────────────┐
 │                   Docker CLI / Client                  │
 └───────────────────────────┬────────────────────────────┘
                             │ REST API over Unix Socket
                             ▼
 ┌────────────────────────────────────────────────────────┐
 │                    Docker Engine (dockerd)              │
 └───────────────────────────┬────────────────────────────┘
                             │ gRPC
                             ▼
 ┌────────────────────────────────────────────────────────┐
 │                        containerd                      │
 └─────────────┬────────────────────────────┬─────────────┘
               │ OCI (Runtime Spec)         │ OCI
               ▼                            ▼
 ┌───────────────────────────┐┌───────────────────────────┐
 │       runc (CPU)          ││ nvidia-container-runtime  │
 ├───────────────────────────┤├───────────────────────────┤
 │ Standard Linux Isolation   ││ Direct Kernel GPU Access  │
 └───────────────────────────┘└───────────────────────────┘
```

---

## 📘 Linux Process Isolation: Core Kernel Primitives

Containers are not virtual machines; they are standard Linux processes running inside isolated kernel sandboxes. This isolation is achieved using three primary Linux kernel features:

### 1. Namespaces (Resource Virtualization)
Namespaces isolate system resources from the containerized process:
* **PID Namespace**: Isolates the process ID space. The container's primary execution starts as PID 1, completely unaware of host system processes.
* **NET Namespace**: Isolates physical and virtual network interfaces, routing tables, and firewall rules.
* **MNT Namespace**: Restricts filesystem mount paths.
* **IPC Namespace**: Disables direct inter-process communication between host and container processes.

### 2. Control Groups v2 (cgroups v2)
cgroups restrict, prioritize, and log resource usage (CPU, RAM, Disk I/O, GPU memory boundaries) for groups of processes. This prevents container workloads from starving host resources.

### 3. Transparent Hugepages (THP) & Memory Allocation
Traditional Linux memory pages are 4KB. For deep learning models loading gigabytes of weights, translating virtual addresses to physical RAM using 4KB chunks creates high translation overhead. 
* **Hugepages**: Pre-allocates high-speed 2MB or 1GB pages in physical RAM, reducing translation lookaside buffer (TLB) cache misses significantly.

---

## 🔌 NVIDIA Container Toolkit Integration & Runtime Setup

To run CUDA acceleration inside a container, the host operating system's standard container engine (`runc`) must be configured to pass physical graphics hardware descriptors (`/dev/nvidia*`) and dynamic CUDA driver libraries directly to the container filesystem.

```
 ┌────────────────────────────────────────┐
 │ GPU Inference Container (vLLM/PyTorch) │
 └───────────────────┬────────────────────┘
                     │ Requests CUDA execution
                     ▼
 ┌────────────────────────────────────────┐
 │      NVIDIA Container Runtime          │
 ├────────────────────────────────────────┤
 │ Intercepts boot and maps:              │
 │ - /dev/nvidia0 (GPU card device)       │
 │ - /dev/nvidia-uvm (Unified memory)    │
 │ - Host CUDA libraries (.so files)      │
 └───────────────────┬────────────────────┘
                     │ Communicates directly
                     ▼
 ┌────────────────────────────────────────┐
 │         NVIDIA GPU Driver (Host)       │
 └────────────────────────────────────────┘
```

### 🛠️ Installation Playbook (Ubuntu/Debian Host)

```bash
# 1. Configure the production package repository
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's|deb https://|deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://|g' | \
  sudo tee /etc/lists.d/nvidia-container-toolkit.list

# 2. Update and install toolkit components
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit

# 3. Register NVIDIA runtime with Docker Engine
sudo nvidia-container-toolkit daemon-setup --runtime=docker

# 4. Restart Docker daemon to apply configuration
sudo systemctl restart docker
```

Once restarted, verify that your `/etc/docker/daemon.json` contains the `nvidia` runtime configuration:
```json
{
  "runtimes": {
    "nvidia": {
      "path": "nvidia-container-runtime",
      "runtimeArgs": []
    }
  }
}
```

---

## 🐳 Docker Compose GPU Deployment Example

Deploy a local Ollama serving engine mapping physical GPU devices to your container:

```yaml
version: '3.8'

services:
  ollama-gpu:
    image: ollama/ollama:latest
    container_name: local-gpu-model-host
    ports:
      - "11434:11434"
    volumes:
      - ollama_cache:/root/.ollama
    # Request physical GPU assignment
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    restart: unless-stopped

volumes:
  ollama_cache:
```

Launch the stack:
```bash
docker compose up -d
```

---

## ⚡ Highly Optimized Multi-Stage PyTorch Dockerfile

Using basic container bases (like standard Ubuntu) results in bloated image sizes (often over 15GB), slowing down deployment times. This multi-stage Dockerfile optimizes layer caches and keeps production artifacts under 3GB:

```dockerfile
# ==========================================
# Stage 1: Build & Dependency compilation
# ==========================================
FROM pytorch/pytorch:2.2.1-cuda12.1-cudnn8-devel AS builder

WORKDIR /build

# Install compilation essentials
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Pre-compile wheel files to cache heavy downloads
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir=/build/wheels -r requirements.txt

# ==========================================
# Stage 2: Minimal Runtime Execution
# ==========================================
FROM pytorch/pytorch:2.2.1-cuda12.1-cudnn8-runtime AS runner

WORKDIR /app

# Enforce secure system environments
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Copy compiled wheel binaries from builder stage
COPY --from=builder /build/wheels /wheels
COPY --from=builder /build/requirements.txt .

# Install wheels without dev dependencies
RUN pip install --no-index --find-links=/wheels -r requirements.txt && \
    rm -rf /wheels requirements.txt

# Copy application codes
COPY src/ /app/src/

# Security: Run as a non-privileged system user
RUN useradd -u 10001 -m appuser && \
    chown -R appuser:appuser /app
USER 10001

EXPOSE 8000

ENTRYPOINT ["python", "src/app.py"]
```

---

## 🔒 Container Security & Production Hardening Rules

1. **Drop Capabilities Programmatically**: Drop all default kernel capabilities, adding back *only* what is necessary (e.g. `CAP_NET_BIND_SERVICE`).
2. **ReadOnly Root Filesystem**: Configure containers with `readOnlyRootFilesystem: true`. Force models to load weights inside dedicated, mounted directories.
3. **No Privilege Escalation**: Enforce standard process parameters:
   ```yaml
   securityContext:
     allowPrivilegeEscalation: false
     runAsNonRoot: true
     runAsUser: 10001
   ```

---

## 📊 Troubleshooting & Diagnostics Playbook

### 💥 Issue: Container Fails with `CUDA driver version is insufficient for CUDA runtime version`
* **Root Cause**: The host operating system's NVIDIA graphics driver is too old to support the target CUDA compilation version inside the container.
* **Mitigation**:
  1. Check host driver version: `nvidia-smi`.
  2. Map the compatibility matrix: A CUDA 12.1 container demands at least host driver `525.60.13` or greater.
  3. Either upgrade your host drivers or rebuild the container using a lower CUDA base image version (e.g. `cuda11.8`).

### 💥 Issue: GPU Not Found inside running container
* **Root Cause**: The Docker daemon was not restarted after installing the NVIDIA Container Toolkit, or the execution command lacked the `--gpus all` parameter.
* **Test Command**:
  ```bash
  docker run --rm --runtime=nvidia --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi
  ```
  If this command successfully outputs your GPU specs, your container runtime setup is functioning perfectly!
