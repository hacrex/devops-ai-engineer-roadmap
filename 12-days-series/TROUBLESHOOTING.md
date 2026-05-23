# 12 Days of AI Infrastructure - Troubleshooting Guide

Common issues and solutions for the 12-days-series curriculum.

## Table of Contents
- [Environment Setup](#environment-setup)
- [Docker & Containers](#docker--containers)
- [Kubernetes](#kubernetes)
- [Python & Dependencies](#python--dependencies)
- [Local LLMs](#local-llms)
- [Hugging Face](#hugging-face)
- [Vector Databases](#vector-databases)
- [AI Agents & MCP](#ai-agents--mcp)
- [Network & Connectivity](#network--connectivity)

---

## Environment Setup

### Issue: Python version mismatch
**Symptom:** `SyntaxError` or dependency installation failures
**Solution:**
```bash
# Check Python version
python --version

# Required: Python 3.9+
# Use pyenv to manage versions if needed
pyenv install 3.10.0
pyenv local 3.10.0
```

### Issue: Virtual environment not activated
**Symptom:** Packages install globally or import errors
**Solution:**
```bash
# Create and activate venv
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Verify activation
which python  # Should point to venv
```

### Issue: Insufficient disk space
**Symptom:** Model downloads fail, Docker builds fail
**Solution:**
```bash
# Check disk space
df -h

# Clean up Docker
docker system prune -a

# Remove old models
rm -rf ~/.cache/huggingface
```

---

## Docker & Containers

### Issue: Docker daemon not running
**Symptom:** `Cannot connect to the Docker daemon`
**Solution:**
```bash
# Linux
sudo systemctl start docker
sudo systemctl enable docker

# Mac/Windows: Start Docker Desktop application

# Verify
docker info
```

### Issue: Permission denied on Docker socket
**Symptom:** `permission denied while trying to connect to the Docker daemon socket`
**Solution:**
```bash
# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Or use sudo (not recommended for production)
sudo docker run ...
```

### Issue: Container exits immediately
**Symptom:** Container starts then stops
**Solution:**
```bash
# Check logs
docker logs <container_id>

# Run interactively for debugging
docker run -it <image> /bin/bash

# Common causes:
# - Missing environment variables
# - Port conflicts
# - Application crashes on startup
```

### Issue: Port already in use
**Symptom:** `Bind for 0.0.0.0:8080 failed: port is already allocated`
**Solution:**
```bash
# Find process using port
lsof -i :8080
# or
netstat -tulpn | grep 8080

# Kill process or use different port
docker run -p 8081:8080 ...
```

---

## Kubernetes

### Issue: kubectl cannot connect to cluster
**Symptom:** `The connection to the server localhost:8080 was refused`
**Solution:**
```bash
# Check cluster status
kubectl cluster-info

# For Minikube
minikube status
minikube start

# For kind
kind get clusters

# Check kubeconfig
echo $KUBECONFIG
cat ~/.kube/config
```

### Issue: Pods stuck in Pending state
**Symptom:** Pod remains in Pending status
**Solution:**
```bash
# Describe pod to see events
kubectl describe pod <pod-name>

# Common causes:
# - Insufficient resources (CPU/memory)
# - No nodes available
# - PersistentVolume claims unsatisfied

# Check node resources
kubectl top nodes
kubectl describe nodes
```

### Issue: CrashLoopBackOff
**Symptom:** Pod repeatedly restarts
**Solution:**
```bash
# Check logs from current and previous instance
kubectl logs <pod-name>
kubectl logs <pod-name> --previous

# Check events
kubectl describe pod <pod-name>

# Common causes:
# - Application error
# - Missing config/secrets
# - Failed health checks
```

### Issue: Service not accessible
**Symptom:** Cannot reach service via ClusterIP/NodePort
**Solution:**
```bash
# Check service endpoints
kubectl get endpoints <service-name>

# Test from within cluster
kubectl run test --rm -it --image=busybox -- /bin/sh
wget <service-name>:<port>

# Check service selector matches pod labels
kubectl get pods --show-labels
kubectl get svc <service-name> -o yaml
```

---

## Python & Dependencies

### Issue: Module not found
**Symptom:** `ModuleNotFoundError: No module named 'xxx'`
**Solution:**
```bash
# Ensure venv is activated
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# For specific day
cd dayXX-topic
pip install -r requirements.txt
```

### Issue: Version conflicts
**Symptom:** Dependency resolution errors
**Solution:**
```bash
# Upgrade pip
pip install --upgrade pip

# Clear cache
pip cache purge

# Reinstall in fresh venv
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: CUDA/GPU not detected
**Symptom:** PyTorch/TensorFlow runs on CPU only
**Solution:**
```bash
# Check CUDA availability
python -c "import torch; print(torch.cuda.is_available())"

# Install correct version
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Check NVIDIA drivers
nvidia-smi
```

---

## Local LLMs

### Issue: Ollama not starting
**Symptom:** `ollama run` fails
**Solution:**
```bash
# Check if Ollama is running
ps aux | grep ollama

# Start Ollama server
ollama serve

# On Linux, ensure systemd service
sudo systemctl start ollama
sudo systemctl enable ollama

# Check logs
journalctl -u ollama -f
```

### Issue: Model download fails
**Symptom:** Timeout or connection error pulling model
**Solution:**
```bash
# Check internet connection
ping huggingface.co

# Set proxy if needed
export HTTPS_PROXY=http://proxy:port

# Try alternative mirror
export HF_ENDPOINT=https://hf-mirror.com

# Download manually and copy
# ~/.ollama/models/
```

### Issue: Out of memory (OOM)
**Symptom:** Model loading fails with OOM error
**Solution:**
```bash
# Check available memory
free -h

# Use smaller model
ollama run llama3.2:1b  # Instead of 70b

# Quantize model
ollama pull llama3.2:q4_0

# Close other applications
# Reduce batch size in code
```

### Issue: Slow inference
**Symptom:** Generation takes too long
**Solution:**
```bash
# Check if using GPU
nvidia-smi

# Enable GPU acceleration
# Ensure CUDA-enabled version installed

# Use smaller context window
# Reduce max_tokens parameter

# Consider quantized models
ollama run llama3.2:q4_k_m
```

---

## Hugging Face

### Issue: Authentication failed
**Symptom:** `401 Client Error: Unauthorized`
**Solution:**
```bash
# Login with token
huggingface-cli login

# Or set environment variable
export HF_TOKEN=your_token_here

# Get token from: https://huggingface.co/settings/tokens
```

### Issue: Rate limiting
**Symptom:** `429 Too Many Requests`
**Solution:**
```bash
# Implement retry logic
from huggingface_hub import HfFolder
import time

# Use authentication for higher limits
huggingface-cli login

# Add delays between requests
time.sleep(1)
```

### Issue: Model not found
**Symptom:** `404 Client Error: Entry Not Found`
**Solution:**
```bash
# Check model name spelling
# Verify model exists on hub

# Some models require access request
# Visit model page and click "Agree and access"

# Check if model is gated
# Requires authentication even if public
```

---

## Vector Databases

### Issue: ChromaDB connection failed
**Symptom:** `ConnectionRefusedError`
**Solution:**
```bash
# Check if ChromaDB is running
# For persistent mode
chroma run --path ./db

# In code, ensure correct host/port
client = chromadb.HttpClient(host='localhost', port=8000)

# Check firewall settings
```

### Issue: Index size too large
**Symptom:** Memory errors during indexing
**Solution:**
```bash
# Use persistent storage
import chromadb
client = chromadb.PersistentClient(path="./chroma_db")

# Batch insertions
for i in range(0, len(docs), 100):
    collection.add(documents=docs[i:i+100])

# Use HNSW index parameters
collection.modify(efConstruction=128, M=16)
```

### Issue: Slow similarity search
**Symptom:** Query takes seconds
**Solution:**
```bash
# Build index explicitly
collection.create_index()

# Adjust HNSW parameters
# Higher efSearch = more accurate but slower

# Limit results
results = collection.query(query_texts=[q], n_results=10)

# Consider using GPU acceleration
```

---

## AI Agents & MCP

### Issue: MCP server not connecting
**Symptom:** Agent cannot find MCP tools
**Solution:**
```bash
# Verify MCP server is running
# Check configuration file

# Example MCP config (~/.mcp.json)
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem"]
    }
  }
}

# Restart agent with updated config
```

### Issue: Tool execution fails
**Symptom:** Agent reports tool error
**Solution:**
```bash
# Check tool permissions
# Verify API keys are set

# Debug tool calls
# Enable verbose logging in agent

# Test tool independently
curl http://api.example.com/endpoint
```

### Issue: Agent loops infinitely
**Symptom:** Agent keeps calling same tool
**Solution:**
```bash
# Set max_iterations parameter
agent = Agent(max_iterations=10)

# Improve prompt instructions
# Add termination conditions

# Review tool descriptions for clarity
```

---

## Network & Connectivity

### Issue: DNS resolution fails
**Symptom:** `Could not resolve host`
**Solution:**
```bash
# Check DNS settings
cat /etc/resolv.conf

# Use public DNS
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf

# Test resolution
nslookup huggingface.co
```

### Issue: Proxy required
**Symptom:** Connection timeout in corporate network
**Solution:**
```bash
# Set proxy variables
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
export NO_PROXY=localhost,127.0.0.1,.local

# For Python
export HF_ENDPOINT=https://huggingface.co
```

### Issue: SSL certificate error
**Symptom:** `SSL: CERTIFICATE_VERIFY_FAILED`
**Solution:**
```bash
# Update certificates
sudo update-ca-certificates  # Debian/Ubuntu
sudo trust extract-compat    # RHEL/Fedora

# For development only (not recommended for production)
export PYTHONREQUESTSCA_BUNDLE=/path/to/cert.pem
```

---

## Getting Help

If issues persist:

1. **Check logs**: Most tools provide detailed logs
2. **Search GitHub Issues**: Many problems already documented
3. **Community forums**: 
   - Stack Overflow (tag: kubernetes, docker, llm)
   - Hugging Face Forums
   - Reddit r/MachineLearning, r/kubernetes
4. **Discord/Slack communities**: Real-time help available

### Useful Debug Commands
```bash
# System resources
htop
nvidia-smi
df -h

# Network
curl -v https://api.example.com
ping 8.8.8.8
traceroute huggingface.co

# Docker
docker ps -a
docker logs <container>
docker inspect <container>

# Kubernetes
kubectl get all -A
kubectl describe pod <pod>
kubectl logs -f <pod>
```

---

## Contributing Fixes

Found a solution not listed here? Please contribute:
1. Open an issue on GitHub
2. Submit a PR adding to this guide
3. Include: symptom, cause, solution, verification steps

Happy troubleshooting! 🛠️
