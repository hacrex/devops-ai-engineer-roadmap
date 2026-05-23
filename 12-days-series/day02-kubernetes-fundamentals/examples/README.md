# Kubernetes Manifest Examples for Day 02

This directory contains Kubernetes YAML manifests for learning fundamentals.

## Files Included

### Basic Pods
- `pod-simple.yaml` - Minimal pod definition
- `pod-with-probes.yaml` - Pod with liveness/readiness probes

### Deployments
- `deployment-basic.yaml` - Simple deployment with replicas
- `deployment-with-resources.yaml` - Deployment with CPU/memory limits

### Services
- `service-clusterip.yaml` - Internal service
- `service-nodeport.yaml` - Externally accessible service
- `service-loadbalancer.yaml` - Cloud load balancer service

### ConfigMaps & Secrets
- `configmap-example.yaml` - Configuration data
- `secret-example.yaml` - Sensitive data (base64 encoded)

### Complete Applications
- `full-app.yaml` - Complete app with deployment, service, configmap

## Usage

```bash
# Apply a manifest
kubectl apply -f pod-simple.yaml

# Apply all manifests in this directory
kubectl apply -f .

# Delete resources
kubectl delete -f pod-simple.yaml
```

## Prerequisites

- Kubernetes cluster (Minikube, Kind, or cloud-based)
- kubectl configured

## Next Steps

After mastering these basics, proceed to:
- Day 07: AI Inference on Kubernetes
- Day 12: Real-world Projects with production deployments
