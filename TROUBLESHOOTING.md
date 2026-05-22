# Troubleshooting Guide - DevOps AI Engineer Roadmap

Common issues and solutions for getting started with the roadmap.

## 🔧 Installation Issues

### Python Dependencies Fail to Install

**Problem:** `pip install -r requirements.txt` fails with errors

**Solutions:**
```bash
# 1. Upgrade pip first
python -m pip install --upgrade pip

# 2. Create fresh virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# 3. Install system dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install python3-dev gcc build-essential

# 4. Try installing one package at a time
pip install click
pip install httpx
# etc.
```

### Docker Commands Fail

**Problem:** `docker: command not found` or permission denied

**Solutions:**
```bash
# Install Docker (Ubuntu/Debian)
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker

# Verify installation
docker --version
docker run hello-world

# If using Docker Desktop on Mac/Windows:
# Ensure Docker Desktop application is running
```

### Ollama Won't Start

**Problem:** `ollama: command not found` or connection refused

**Solutions:**
```bash
# Reinstall Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Check if service is running
systemctl status ollama
# or
ps aux | grep ollama

# Start manually
ollama serve &

# Test connection
curl http://localhost:11434/api/tags

# Check logs
journalctl -u ollama -f
```

## 🤖 Local LLM Issues

### Model Download Fails or Times Out

**Problem:** `ollama pull qwen2.5-coder:7b` hangs or fails

**Solutions:**
```bash
# 1. Check internet connection
ping ollama.com

# 2. Use mirror/regional endpoint (if available)
export OLLAMA_DOWNLOAD_URL=https://mirror.example.com

# 3. Download model file manually and import
wget <model-url> -O model.bin
ollama create qwen2.5-coder:7b -f ./Modelfile

# 4. Try smaller model first
ollama pull tinyllama
ollama pull phi3

# 5. Check disk space
df -h
# Need 4-8GB per 7B parameter model
```

### Out of Memory Errors

**Problem:** `CUDA out of memory` or system freezes during inference

**Solutions:**
```bash
# 1. Use smaller quantized models
ollama pull qwen2.5-coder:7b-q4_K_M  # 4-bit quantized

# 2. Limit GPU memory usage
export OLLAMA_NUM_GPU=1
export OLLAMA_MAX_VRAM=4000000000  # 4GB limit

# 3. Use CPU-only mode (slower but works)
export OLLAMA_NUM_GPU=0

# 4. Close other applications
# Free up RAM before running

# 5. Monitor resources
watch -n 1 'free -h && nvidia-smi'
```

### Slow Inference Performance

**Problem:** Responses take too long (>30 seconds)

**Solutions:**
```bash
# 1. Use smaller/faster models
ollama pull phi3:mini        # 3.8B, very fast
ollama pull mistral:7b       # Good balance

# 2. Enable GPU acceleration
# Ensure NVIDIA drivers installed
nvidia-smi

# 3. Reduce context length
# In your code, set max_tokens lower

# 4. Use quantized models (4-bit or 5-bit)
ollama pull llama3.2:3b-q4_K_M

# 5. Batch requests when possible
```

## 🐳 Kubernetes Issues

### Minikube/Kubernetes Cluster Won't Start

**Problem:** `minikube start` fails

**Solutions:**
```bash
# 1. Check virtualization enabled
grep -E --color 'vmx|svm' /proc/cpuinfo

# 2. Increase allocated resources
minikube start --memory=4096 --cpus=2

# 3. Use different driver
minikube start --driver=docker

# 4. Delete and recreate
minikube delete
minikube start

# 5. Check logs
minikube logs
```

### Pod Won't Start or Crashes

**Problem:** Pods in `CrashLoopBackOff` or `Error` state

**Solutions:**
```bash
# Check pod status
kubectl get pods
kubectl describe pod <pod-name>

# View logs
kubectl logs <pod-name>
kubectl logs <pod-name> --previous  # If crashed

# Common fixes:
# 1. Check resource limits
kubectl edit deployment/<name>

# 2. Verify image exists and is accessible
docker pull <image-name>

# 3. Check ConfigMaps and Secrets
kubectl get configmaps
kubectl get secrets

# 4. Test locally first
docker run <image-name>
```

## 📦 Project-Specific Issues

### AI DevOps Copilot Not Generating Output

**Problem:** `python copilot.py generate` returns empty or errors

**Solutions:**
```bash
# 1. Verify Ollama is running
curl http://localhost:11434/api/tags

# 2. Check model is available
ollama list | grep qwen

# 3. Test Ollama directly
ollama run qwen2.5-coder:7b "print('hello')"

# 4. Check config.yaml
cat config.yaml
# Ensure ollama_url is correct

# 5. Run with verbose output
python copilot.py generate kubernetes --prompt "nginx" --verbose

# 6. Check Python version
python --version  # Need 3.9+
```

### Local RAG Assistant Returns No Results

**Problem:** Queries return empty or irrelevant results

**Solutions:**
```bash
# 1. Verify documents were ingested
# Check the ingestion logs

# 2. Test embedding model
python -c "from sentence_transformers import SentenceTransformer; m = SentenceTransformer('all-MiniLM-L6-v2'); print(m.encode('test'))"

# 3. Check vector database
# Access ChromaDB/Weaviate UI if available

# 4. Re-ingest documents
python app.py ingest --force

# 5. Adjust similarity threshold
# In config, lower the threshold temporarily

# 6. Verify document format
# Ensure PDFs/TXTs are readable
```

## 🔐 Permission Issues

### Cannot Write to Directory

**Problem:** `Permission denied` errors

**Solutions:**
```bash
# Fix ownership (Linux/Mac)
sudo chown -R $USER:$USER /workspace

# Fix permissions
chmod -R u+w /workspace

# Or run with sudo (not recommended for development)
sudo python script.py
```

### Docker Permission Denied

**Problem:** `Got permission denied while trying to connect to the Docker daemon`

**Solutions:**
```bash
# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Verify
docker run hello-world

# Alternative: use sudo (not ideal)
sudo docker run hello-world
```

## 🌐 Network Issues

### Cannot Pull Images or Models

**Problem:** Connection timeouts or DNS failures

**Solutions:**
```bash
# 1. Test connectivity
ping google.com
ping ollama.com

# 2. Configure DNS
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf

# 3. Use proxy if behind corporate firewall
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080

# 4. Configure Docker proxy
# Edit /etc/docker/daemon.json
{
  "proxies": {
    "http-proxy": "http://proxy.example.com:8080",
    "https-proxy": "http://proxy.example.com:8080"
  }
}

# 5. Try alternative registries/mirrors
```

## 📊 Resource Monitoring

### Check System Resources

```bash
# Memory and swap
free -h

# Disk space
df -h

# CPU usage
top
# or
htop

# GPU (if NVIDIA)
nvidia-smi

# Docker resources
docker stats

# Kubernetes resources
kubectl top nodes
kubectl top pods
```

## 🆘 Still Stuck?

If none of the above solutions work:

1. **Check Logs:**
   ```bash
   # Application logs
   journalctl -xe
   
   # Docker logs
   docker logs <container-id>
   
   # Kubernetes logs
   kubectl logs <pod-name> --all-containers
   ```

2. **Search Existing Issues:**
   - GitHub Issues in this repository
   - Stack Overflow with relevant tags
   - Official documentation for tools (Ollama, Kubernetes, etc.)

3. **Create a New Issue:**
   Include:
   - Exact error messages
   - Steps to reproduce
   - Your environment (OS, Python version, Docker version)
   - What you've already tried
   - Relevant log excerpts

4. **Community Support:**
   - Open a GitHub Discussion
   - Check Discord/Slack communities for specific tools
   - Ask on Reddit r/devops or r/MachineLearning

## 📝 Quick Diagnostic Script

Run this to gather system info:

```bash
#!/bin/bash
echo "=== System Info ==="
uname -a
echo ""
echo "=== Python Version ==="
python --version
echo ""
echo "=== Docker Version ==="
docker --version
echo ""
echo "=== Ollama Status ==="
ollama --version 2>/dev/null || echo "Ollama not installed"
echo ""
echo "=== Memory ==="
free -h
echo ""
echo "=== Disk Space ==="
df -h /workspace
echo ""
echo "=== GPU (if available) ==="
nvidia-smi 2>/dev/null || echo "No NVIDIA GPU detected"
```

Save as `diagnose.sh`, run with `bash diagnose.sh`, and share output when asking for help.

---

**Remember:** Most issues are solvable! Take it step by step, check logs carefully, and don't hesitate to ask for help with detailed information.
