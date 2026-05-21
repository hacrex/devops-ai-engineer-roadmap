# 💾 High-Throughput Storage & Kubernetes CSI for AI Platforms

Large Language Models (LLMs) and deep learning models consist of huge files—often spanning from 5GB to over 500GB for a single model (like Llama-3-70B). During startup, fine-tuning, or checkpointing, high-speed disk I/O is critical. A delay in loading model weights into GPU memory directly increases pod initialization times and creates costly GPU idle time. 

---

## 🏗️ Storage Architecture for AI Runtimes

```
                                  ┌────────────────────────┐
                                  │   Inference Engine     │
                                  │   (vLLM / PyTorch Pod) │
                                  └───────────┬────────────┘
                                              │
                      ┌───────────────────────┴───────────────────────┐
                      ▼ Persistent Volume Claim (PVC)                 ▼ PVC
          ┌────────────────────────┐                      ┌────────────────────────┐
          │  High-Speed Local NVMe │                      │   Distributed Object   │
          │  (Local Path / Host)   │                      │  (Rook/Ceph / MinIO)   │
          ├────────────────────────┤                      ├────────────────────────┤
          │ - Best for weight cache│                      │ - Best for model pool  │
          │ - 3GB/sec+ read speed  │                      │ - Shared across nodes  │
          │ - Single node tied     │                      │ - S3-compatible API    │
          └────────────────────────┘                      └────────────────────────┘
```

---

## 📘 Storage Concepts for DevOps AI Engineers

### 1. Kubernetes Container Storage Interface (CSI)
The CSI allows third-party storage providers to write plugins for Kubernetes without modifying core Kubernetes code. 
* **Why it matters for AI**: High-performance CSI plugins (like Rook/Ceph or AWS EBS gp3/io2) let pod runtimes dynamically provision high-IOPS block storage with features like fast snapshots and volume cloning for quick model version rollbacks.

### 2. Local-Path / Local Persistent Volumes vs. Shared Storage
* **Local Volumes (NVMe)**: Offer direct-attach disk read/write performance. This is the gold standard for **LLM weight caching**. vLLM downloads the model once to a fast local NVMe volume; subsequent cold restarts read the model in seconds.
* **Shared Storage (CephFS/NFS)**: Allow multiple pods to attach to the same storage volume (`ReadWriteMany`). Ideal for sharing training datasets across multi-node distributed training clusters, though they introduce slight latency overhead.

---

## 🛠️ Hands-on Storage Lab: MinIO Model Store Setup

In this lab, you will spin up a local S3-compatible MinIO object store via Docker Compose, write a Python script to programmatically upload/download large model weight tensors, and write a Kubernetes PV/PVC configuration.

### Step 1: Run MinIO Object Store using Docker Compose
Create a `docker-compose.yml` for MinIO:
```yaml
version: '3.7'
services:
  minio:
    image: minio/minio:RELEASE.2024-02-09T06-00-14Z
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      MINIO_ROOT_USER: admin
      MINIO_ROOT_PASSWORD: SuperSecurePassword123
    volumes:
      - minio_data:/data
    command: server /data --console-address ":9001"

volumes:
  minio_data:
```
Run `docker-compose up -d` to launch MinIO.

### Step 2: Upload/Download Model Weights via Python
Install the MinIO client SDK: `pip install minio`.
Create a python script `model_sync.py`:
```python
import os
from minio import Minio
from minio.error import S3Error

# 1. Initialize MinIO Client
client = Minio(
    "localhost:9000",
    access_key="admin",
    secret_key="SuperSecurePassword123",
    secure=False
)

bucket_name = "model-registry"

try:
    # 2. Create bucket if not exists
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
        print(f"Bucket '{bucket_name}' created successfully.")
    
    # 3. Simulate and upload a mock model weight file (10MB)
    mock_weights_path = "mock_model.bin"
    with open(mock_weights_path, "wb") as f:
        f.write(os.urandom(10 * 1024 * 1024)) # 10MB of random bytes
        
    print("Uploading mock model weights to MinIO...")
    client.fput_object(bucket_name, "llama-3-8b/mock_model.bin", mock_weights_path)
    print("Upload complete!")

    # 4. Download it back to simulate a pod pulling the model
    print("Downloading model weights for local inference...")
    client.fget_object(bucket_name, "llama-3-8b/mock_model.bin", "downloaded_model.bin")
    print("Download complete! Model ready for GPU loading.")

    # Cleanup local files
    os.remove(mock_weights_path)
    os.remove("downloaded_model.bin")

except S3Error as exc:
    print("S3 operation failed:", exc)
```
Run `python model_sync.py` to test the storage pipeline.

---

## ⚡ Production Kubernetes Storage YAML

Below is a production-ready manifest creating a high-speed, NVMe-backed custom StorageClass and a PVC to mount local NVMe storage onto your vLLM model cache directory:

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: nvme-high-iops
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
parameters:
  type: pd-ssd # For Google Cloud, or gp3 for AWS
  iops: "10000"
  throughput: "500" # 500 MB/s limit

---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: vllm-model-cache-pvc
  namespace: ai-platform
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: nvme-high-iops
  resources:
    requests:
      storage: 100Gi # Large enough to cache multiple HuggingFace models
```

---

## 🔒 Security Considerations
1. **Encryption at Rest**: Ensure your Cloud Provider or local Rook/Ceph storage class is configured with KMS integration to encrypt model weights at rest.
2. **Access Control**: Keep your MinIO or AWS S3 credentials out of code! Mount them dynamically into containers using Kubernetes Secrets or IAM Roles for Service Accounts (IRSA).
3. **Volume Permission Boundary**: Set proper `securityContext` parameters in your Pod specification to restrict write access to the mounted volume to only the application process UID.

---

## 📈 Scaling & Observability Considerations
* **Storage IOPS Bottlenecks**: Monitor disk throughput and IOPS using Prometheus (`node_disk_read_bytes_total` and `node_disk_writes_completed_total`). High IOPS exhaustion will cause inference container replicas to freeze during scales.
* **WaitForFirstConsumer**: Always set `volumeBindingMode: WaitForFirstConsumer` on local storage classes. This ensures Kubernetes only schedules/binds the Persistent Volume *after* a pod is assigned to a specific GPU node, preventing scheduling deadlocks.

---

## 🔍 Troubleshooting Guide

### 💥 Issue: Kubernetes Pod Stuck in `ContainerCreating` or `VolumeBinding`
* **Root Cause**: The storage class lacks the required volume capacity on the targeted node, or the physical storage device failed to mount.
* **Diagnostic Command**:
  ```bash
  # View exact scheduler issues causing volume mount failure
  kubectl describe pod <pod-name> -n ai-platform
  ```
* **Mitigation**:
  1. Check if the PV exists and is in `Available` status.
  2. Verify if the targeted node matches the `nodeAffinity` constraints set on the manual PV.
  3. Inspect kernel logs on the host to check for physical NVMe drive errors (`dmesg | grep -E "nvme|sd"`).

---

## 🌟 Best Practices & Open-Source Tools
* **Rook/Ceph**: Use Rook to manage a Ceph cluster inside Kubernetes, converting empty node drives into a robust, high-performance distributed storage mesh.
* **Model Cache Pre-Warming**: Create a Kubernetes `DaemonSet` or `InitContainer` to pull heavy model weight layers onto node NVMe storage caches *before* triggering actual app deployments, ensuring instant container startup speeds.
