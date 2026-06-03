# 🚀 Quick Start Guide - DevOps AI Engineer Roadmap

Get up and running in **15 minutes** with hands-on AI/DevOps integration!

## ⚡ Fastest Path to Results

### Option 1: Try a Local LLM (5 minutes)

```bash
# Install Ollama (Linux/Mac)
curl -fsSL https://ollama.com/install.sh | sh

# Pull a lightweight model
ollama pull qwen2.5-coder:7b

# Test it
ollama run qwen2.5-coder:7b "Write a Python function to check if a port is open"
```

### Option 2: Run the AI DevOps Copilot (10 minutes)

```bash
# Navigate to project
cd projects/ai-devops-copilot

# Install dependencies
pip install -r requirements.txt

# Ensure Ollama is running
ollama serve &

# Generate a Kubernetes manifest
python copilot.py generate kubernetes --prompt "nginx deployment with 3 replicas"
```

### Option 3: Deploy Local RAG Assistant (15 minutes)

```bash
cd projects/local-rag-assistant

# Install dependencies
pip install -r requirements.txt

# Start with Docker Compose
docker-compose up -d

# Access the web UI
open http://localhost:8501
```

## 📋 Prerequisites Checklist

- [ ] Python 3.9+ installed (`python --version`)
- [ ] Docker & Docker Compose (`docker --version`)
- [ ] Git (`git --version`)
- [ ] 8GB+ RAM recommended for local LLMs
- [ ] 20GB+ free disk space

## 🎯 Your First Learning Path

### Day 1: Foundation (30 min)
1. Read [Day 01: Linux & Containers](12-days-series/day01-linux-containers/)
2. Complete the containerization exercise
3. ✅ Check off items in the learning checklist

### Day 2: Kubernetes Basics (45 min)
1. Read [Day 02: Kubernetes Fundamentals](12-days-series/day02-kubernetes-fundamentals/)
2. Deploy your first pod
3. Run the hands-on lab

### Day 3: Python Automation (45 min)
1. Read [Day 03: Python for DevOps](12-days-series/day03-python-automation/)
2. Write your first automation script
3. Test with the provided examples

## 🔧 Common Commands

```bash
# Check system resources (for LLM inference)
free -h && df -h

# Verify Ollama is running
curl http://localhost:11434/api/tags

# List available models
ollama list

# Run tests for any project
cd projects/<project-name>
make test
```

## 🆘 Need Help?

- 📖 Full documentation: [README.md](README.md)
- 📚 Deeper study resources: [STUDY_MATERIALS.md](STUDY_MATERIALS.md)
- 🐛 Found an issue? [Open an Issue](https://github.com/your-repo/issues)
- 💬 Questions? Check [Troubleshooting Guide](TROUBLESHOOTING.md)
- 🤝 Want to contribute? See [CONTRIBUTING.md](CONTRIBUTING.md)

## 🎓 Next Steps

After completing the quick start:

1. **Pick a learning track:**
   - 🟢 Beginner: Start with [12 Days Series](12-days-series/README.md)
   - 🟡 Intermediate: Try [AI Agents](ai-agents/)
   - 🔴 Advanced: Build [Production Projects](projects/)

2. **Join the community:**
   - Star this repo to support the project ⭐
   - Share your progress on social media
   - Contribute improvements via PR

3. **Build something real:**
   - Fork this repo
   - Customize a project for your needs
   - Deploy to your cloud environment

---

**💡 Pro Tip:** Don't try to learn everything at once. Focus on one module per day, complete the hands-on labs, and build incrementally.

**Ready?** Pick your starting point above and let's go! 🚀
