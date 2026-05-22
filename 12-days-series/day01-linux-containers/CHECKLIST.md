# 📋 Day 01: Linux & Containers - Learning Checklist

Complete each item and check it off as you progress!

## 🎯 Learning Objectives

By the end of this module, you will:
- [ ] Understand Linux namespaces and cgroups
- [ ] Be able to create and manage Docker containers
- [ ] Know how to write Dockerfiles
- [ ] Understand container networking basics

## ✅ Pre-Assessment

Before starting, rate your confidence (1-5):

- [ ] I can explain what a container is
- [ ] I have used Docker before
- [ ] I understand Linux process isolation
- [ ] I can write a basic Dockerfile

## 📚 Core Content

### 1. Linux Fundamentals (30 minutes)

- [ ] Read about Linux namespaces
- [ ] Read about control groups (cgroups)
- [ ] Understand union filesystems
- [ ] Complete: Run `unshare` command to create namespace

**Hands-on:**
```bash
# Try creating a new namespace
unshare --pid --fork --mount-proc /bin/bash

# Inside the new namespace, check processes
ps aux
```

### 2. Docker Basics (45 minutes)

- [ ] Install Docker (if not already installed)
- [ ] Run your first container: `docker run hello-world`
- [ ] Pull an image: `docker pull nginx`
- [ ] Run a container with port mapping
- [ ] Inspect a running container

**Hands-on:**
```bash
# Run nginx container
docker run -d -p 8080:80 --name my-nginx nginx

# Verify it's running
curl http://localhost:8080

# Check logs
docker logs my-nginx
```

### 3. Writing Dockerfiles (60 minutes)

- [ ] Understand Dockerfile instructions
- [ ] Create a Dockerfile for a simple Python app
- [ ] Build the image
- [ ] Test the container

**Hands-on:**
```dockerfile
# Create this file as Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```

```bash
# Build and run
docker build -t my-python-app .
docker run my-python-app
```

### 4. Container Networking (30 minutes)

- [ ] Understand bridge network
- [ ] Create a custom network
- [ ] Connect multiple containers
- [ ] Test container-to-container communication

**Hands-on:**
```bash
# Create network
docker network create my-network

# Run containers on same network
docker run -d --name db --network my-network postgres
docker run -d --name app --network my-network my-python-app
```

## 🧪 Lab Exercises

### Lab 1: Containerize a Web Server ⭐

**Task:** Create a Dockerfile for nginx with custom HTML

- [ ] Create `index.html` with your name
- [ ] Write Dockerfile that copies the HTML
- [ ] Build and run the container
- [ ] Access it via browser

**Success Criteria:**
- [ ] Container starts without errors
- [ ] Custom page is visible at localhost:8080
- [ ] Can explain each line in Dockerfile

### Lab 2: Multi-Container Setup ⭐⭐

**Task:** Set up app + database with Docker Compose

- [ ] Write docker-compose.yml
- [ ] Define service dependencies
- [ ] Configure environment variables
- [ ] Start all services
- [ ] Verify connectivity

**Success Criteria:**
- [ ] Both containers start successfully
- [ ] App can connect to database
- [ ] Data persists after restart

### Lab 3: Debug Container Issues ⭐⭐⭐

**Task:** Fix a broken Dockerfile

Given a broken Dockerfile, identify and fix issues:
- [ ] Identify missing dependencies
- [ ] Fix path issues
- [ ] Optimize layer caching
- [ ] Reduce image size

## 📝 Knowledge Check

Answer these questions (answers in solutions/):

1. What is the difference between a VM and a container?
   - [ ] I can explain this clearly

2. What happens when you run `docker run`?
   - [ ] I can describe the steps

3. Why use multi-stage builds?
   - [ ] I understand the benefits

4. How do containers communicate?
   - [ ] I can explain networking options

## 🎓 Post-Assessment

After completing this module, rate your confidence (1-5):

- [ ] I can explain what a container is
- [ ] I have used Docker before
- [ ] I understand Linux process isolation
- [ ] I can write a basic Dockerfile

**Compare with pre-assessment - did your confidence improve?**

## 🚀 Challenge Tasks

Try these for extra practice:

- [ ] Create a Dockerfile under 100MB for a Python app
- [ ] Set up health checks in Dockerfile
- [ ] Use Docker volumes for data persistence
- [ ] Implement logging best practices
- [ ] Create a CI/CD pipeline that builds Docker images

## 📚 Additional Resources

- [ ] Watch: Docker in 100 Seconds (YouTube)
- [ ] Read: Docker documentation on best practices
- [ ] Explore: Docker Hub for official images
- [ ] Join: Docker community forums

## 🤝 Reflection

Take 5 minutes to reflect:

- [ ] What was the most challenging concept?
- [ ] What surprised you about containers?
- [ ] How will you use this in your work?
- [ ] What do you want to learn next?

**Write down your reflections:**

```
Your notes here...
```

## ➡️ Next Steps

Once you've checked all items:

1. Review any unchecked items
2. Complete at least 2 lab exercises
3. Move to [Day 02: Kubernetes Fundamentals](../day02-kubernetes-fundamentals/)

---

**Estimated Time:** 3-4 hours  
**Difficulty:** Beginner  
**Prerequisites:** Basic Linux command line knowledge

**Need Help?** Check [TROUBLESHOOTING.md](../../TROUBLESHOOTING.md) or open a GitHub Discussion!
