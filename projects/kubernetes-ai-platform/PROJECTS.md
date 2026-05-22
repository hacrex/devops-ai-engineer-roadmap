# Kubernetes AI Platform - Project Structure

This project demonstrates deploying AI workloads on Kubernetes with GPU support.

## 📁 Directory Structure

```
kubernetes-ai-platform/
├── README.md                 # Project documentation
├── terraform-gke-gpu/        # Terraform configs for GKE with GPU
│   ├── main.tf              # GKE cluster definition
│   └── variables.tf         # Input variables
├── keda-scaler.yaml          # KEDA autoscaling configuration
└── vllm-kserve.yaml          # KServe deployment for vLLM
```

## 🚀 Quick Start

### 1. Provision GKE Cluster with GPU

```bash
cd terraform-gke-gpu

# Initialize Terraform
terraform init

# Review plan
terraform plan

# Apply configuration
terraform apply
```

### 2. Deploy AI Inference Service

```bash
# Apply KServe deployment
kubectl apply -f vllm-kserve.yaml

# Apply KEDA autoscaler
kubectl apply -f keda-scaler.yaml
```

### 3. Verify Deployment

```bash
# Check pods
kubectl get pods -n ai-inference

# Check services
kubectl get svc -n ai-inference

# Monitor autoscaling
kubectl get keda scaledobject -n ai-inference
```

## 🔧 Makefile Commands

```bash
make provision    # Provision GKE cluster with Terraform
make deploy       # Deploy AI workloads to Kubernetes
make test         # Run validation tests
make clean        # Destroy infrastructure
make monitor      # Open monitoring dashboards
```

## 📊 Architecture

The platform includes:
- **GKE Cluster** with NVIDIA GPU node pools
- **KServe** for model serving
- **KEDA** for event-driven autoscaling
- **vLLM** for high-throughput LLM inference
- **Prometheus + Grafana** for monitoring

## 🎯 Use Cases

1. **LLM Inference Service**: Deploy large language models with auto-scaling
2. **Batch Processing**: Run AI workloads with KEDA-triggered scaling
3. **Multi-tenant AI Platform**: Serve multiple teams with isolated namespaces

## 📝 Configuration

Edit `terraform-gke-gpu/variables.tf` to customize:
- GPU type and count
- Node pool size
- Region/zone
- Network configuration

## 🧪 Testing

```bash
# Test GPU availability
kubectl run gpu-test --image=nvidia/cuda:12.0-base --restart=Never -- nvidia-smi

# Test model endpoint
curl http://<service-ip>/v1/completions \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello", "max_tokens": 100}'
```

## 🗑️ Cleanup

```bash
# Remove Kubernetes resources
kubectl delete -f vllm-kserve.yaml
kubectl delete -f keda-scaler.yaml

# Destroy GKE cluster
cd terraform-gke-gpu
terraform destroy
```

## ⚠️ Cost Considerations

GPU instances are expensive. Always:
- Set up budget alerts in GCP
- Use spot/preemptible instances when possible
- Destroy resources when not in use
- Monitor usage with `gcloud billing accounts list`

## 📚 Resources

- [GKE GPU Guide](https://cloud.google.com/kubernetes-engine/docs/how-to/gpus)
- [KServe Documentation](https://kserve.github.io/website/)
- [KEDA Documentation](https://keda.sh/docs/)
- [vLLM Documentation](https://docs.vllm.ai/)
