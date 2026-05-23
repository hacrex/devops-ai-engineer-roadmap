# AI Inference on Kubernetes - Examples

This directory contains Kubernetes manifests and code examples for deploying AI models.

## Files Included

### Kubernetes Manifests
- `inference-deployment.yaml` - LLM inference server deployment
- `inference-service.yaml` - Service to expose inference API
- `gpu-node-selector.yaml` - Example with GPU node selection
- `model-pvc.yaml` - PersistentVolumeClaim for model storage

### Python Examples
- `k8s_inference_client.py` - Client to call deployed model
- `batch_inference.py` - Batch processing example

## Prerequisites

- Kubernetes cluster with GPU support (optional)
- kubectl configured
- NVIDIA device plugin (for GPU workloads)

## Quick Start

```bash
# Deploy inference server
kubectl apply -f inference-deployment.yaml
kubectl apply -f inference-service.yaml

# Check status
kubectl get pods
kubectl get svc

# Test inference
python k8s_inference_client.py
```

## GPU Configuration

For GPU-enabled deployments:

1. Install NVIDIA device plugin:
```bash
kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/main/deployments/static/nvidia-device-plugin.yml
```

2. Use GPU node selector in deployment YAML

3. Request GPU resources in pod spec:
```yaml
resources:
  limits:
    nvidia.com/gpu: 1
```

## Scaling

See Day 10 (Observability) for monitoring and auto-scaling configurations.
