# 🐧 Linux Internals & Systems Performance Engineering

To design and manage high-performance infrastructure for running AI models, a DevOps AI Engineer must master Linux OS internals. Large Language Models (LLMs) push the boundaries of CPU scheduling, GPU driver interfaces, memory bandwidth, and file system I/O. 

---

## 🏗️ Architectural Overview: Linux Kernel & User Space

The separation between User Space (where containers, databases, and LLM servers run) and Kernel Space (which manages CPU, RAM, and PCIe/NVLink channels to the GPUs) is crucial for systems tuning.

```
┌─────────────────────────────────────────────────────────────┐
│ USER SPACE (Applications & Containers)                      │
│ - PyTorch / vLLM Engine  - Qdrant Vector DB   - Ollama API  │
└──────────────────────────────┬──────────────────────────────┘
                               │ System Calls (syscalls)
                               ▼ (e.g., clone, mmap, io_submit)
┌─────────────────────────────────────────────────────────────┐
│ KERNEL SPACE (Hardware Management & Virtualization)         │
│ - cgroups v2             - Process Scheduler  - Virtual Mem │
│ - Host GPU Drivers       - eBPF Runtime       - File System │
└──────────────────────────────┬──────────────────────────────┘
                               │ Hardware Control
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ PHYSICAL HARDWARE                                           │
│ - AMD EPYC / Intel CPU   - NVIDIA H100 GPU    - NVMe SSD    │
└─────────────────────────────────────────────────────────────┘
```

---

## 📘 Core Systems Engineering Concepts

### 1. Control Groups v2 (cgroups v2)
Control groups manage the resource allocation (CPU, RAM, I/O, PIDs) of containerized workloads. In cgroups v2, the unified hierarchy allows more stable memory pressure management.
* **Why it matters for AI**: If a Python-based PyTorch container exceeds its memory limits, the kernel's OOM (Out Of Memory) Killer immediately terminates the training/inference job.

### 2. Virtual Memory & Hugepages
By default, the Linux kernel manages virtual memory in 4KB pages. For AI workloads with massive tensor parameters in-memory (e.g., a 70B parameter model needing 140GB+ RAM), looking up billions of 4KB pages creates severe TLB (Translation Lookaside Buffer) misses.
* **Solution**: **Transparent Hugepages (THP)** or **Static Hugepages** (2MB to 1GB sizes) reduce page table sizes and memory translation overhead.

### 3. eBPF (Extended Berkeley Packet Filter)
eBPF runs sandboxed programs inside the Linux kernel without changing kernel source or loading modules. It enables zero-overhead observability, advanced networking, and real-time security auditing.
* **Why it matters for AI**: eBPF allows SREs to monitor real-time GPU/CPU context switches and trace network transfer bottlenecks between distributed GPU nodes.

---

## 🛠️ Hands-on Systems Performance Lab

In this lab, you will diagnose system load, investigate memory pressure, trace system calls, and enable Hugepages on a host system.

### Step 1: Diagnose System Load and Hardware Resource Saturation
Run these commands to see CPU bottlenecks, I/O wait times, and swap usage:
```bash
# 1. Check overall CPU and memory utilization (classic tool)
htop

# 2. View virtual memory statistics, page-ins, page-outs, and CPU context switches every 2 seconds
vmstat 2 5

# 3. Analyze disk I/O utilization and queue wait times
iostat -xz 2 5
```

### Step 2: Trace System Calls on a running Inference Server
If a model inference API hangs or crashes, use `strace` to trace the system calls the process is making:
```bash
# Get PID of your Python/vLLM application
PID=$(pgrep -f "vllm")

# Trace file read and write system calls, showing execution timestamps
sudo strace -e trace=openat,read,write,mmap -p $PID -c
```

### Step 3: Configure 2MB Static Hugepages for AI Memory Speedups
To optimize Python PyTorch or C++ llama.cpp runtimes for large memory address mapping:
```bash
# 1. Check current hugepages status
grep HugePages /proc/meminfo

# 2. Set the number of 2MB hugepages to pre-allocate (e.g., 8192 pages = 16GB RAM)
sudo sysctl -w vm.nr_hugepages=8192

# 3. Make hugepage allocations persistent across reboots
echo "vm.nr_hugepages=8192" | sudo tee -a /etc/sysctl.conf
```

---

## ⚡ Production Infrastructure Code

### Terraform GPU VM Provisioning (GCP)
Here is a production-grade Terraform script to spin up a high-performance VM on Google Cloud with an NVIDIA L4 GPU, running on a custom Ubuntu OS image configured for AI payloads:

```hcl
provider "google" {
  project = var.gcp_project_id
  region  = "us-central1"
  zone    = "us-central1-a"
}

resource "google_compute_instance" "gpu_inference_node" {
  name         = "ai-infra-l4-node"
  machine_type = "g2-standard-8" # 8 vCPUs, 32GB RAM

  guest_accelerator {
    type  = "nvidia-l4"
    count = 1
  }

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-lts"
      size  = 200 # 200GB NVMe storage
      type  = "pd-ssd"
    }
  }

  network_interface {
    network = "default"
    access_config {
      // Allocate ephemeral public IP
    }
  }

  scheduling {
    on_host_maintenance = "TERMINATE" # Required for GPU instances in GCP
    automatic_restart   = true
  }

  metadata_startup_script = <<-EOT
    #!/bin/bash
    # 1. Update OS and install dependencies
    apt-get update && apt-get upgrade -y
    apt-get install -y build-essential linux-headers-$(uname -r) docker.io

    # 2. Install NVIDIA CUDA Drivers and Container Toolkit
    distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
    curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
    curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
      sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
      tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
    
    apt-get update && apt-get install -y nvidia-container-toolkit
    nvidia-ctk runtime configure --runtime=docker
    systemctl restart docker

    # 3. Configure Virtual Memory for AI workloads
    sysctl -w vm.max_map_count=262144
    sysctl -w vm.overcommit_memory=1
  EOT
}
```

---

## 🔒 Security Considerations
1. **Unprivileged Namespaces**: Never run containerized AI runtimes as `root` user in User space. Use Docker rootless mode or Kubernetes SecurityContext to run as UID `1000`.
2. **GPU Driver Sandbox Isolation**: Restrict host CUDA device file permissions (`/dev/nvidia*`) using Linux `udev` rules so only authorized container instances can tap into host GPU hardware.
3. **Audit System Calls**: Apply `seccomp` profiles to restrict standard container capabilities. Block unused, high-risk system calls (`kexec_load`, `sys_ptrace`).

---

## 📈 Scaling & Observability Considerations
* **Context Switches**: If you run multiple LLM inference threads on a single VM, keep an eye on *context switches* (`vmstat` -> `cs`). Excess switches cause high latency. Standardize on single-process, highly async runtime engines (like vLLM).
* **eBPF Monitoring**: Run `bpftrace` to capture high-resolution latency distributions of disk reads when fetching model weight tensors (`.safetensors`) from local NVMe cache.

---

## 🔍 Troubleshooting Guide

### 💥 Issue: Container Exits with Exit Code 137 (OOM Killed)
* **Root Cause**: The Python PyTorch/llama.cpp application exceeded the container limits specified in `cgroups` (Docker memory limits or Kubernetes limit settings).
* **Diagnostic Command**:
  ```bash
  # Check kernel system log for Out of Memory events
  dmesg -T | grep -i oom
  ```
* **Mitigation**:
  1. Increase the container memory limits in your YAML.
  2. Implement Model Quantization (e.g., convert FP16 models to 4-bit AWQ or GGUF) to drop RAM consumption by 70%+.
  3. Set environment variable `MALLOC_ARENA_MAX=2` in Python to prevent excessive C-level memory fragmentation.

---

## 🌟 Best Practices & Open-Source Tools
* **Sysstat (`sar`, `iostat`)**: Keep system statistics enabled persistently to capture performance baselines.
* **Vector.dev**: Use Vector to collect Linux `/var/log/syslog` logs and system metrics, piping them efficiently to OpenSearch or Grafana.
* **Static Allocations**: Pre-allocate swap file partitions on ultra-fast NVMe storage if you are running massive model loading workflows to act as a buffer against hard RAM crashes.
