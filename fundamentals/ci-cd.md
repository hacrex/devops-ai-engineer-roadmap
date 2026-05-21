# 🔄 Continuous Integration & Continuous Delivery (CI/CD) & GitOps for AI

Deploying traditional stateless microservices relies on compiling code and running simple unit tests. In **AI Engineering**, CI/CD must also account for massive container layers, complex compiled CUDA dependencies, static security audits of Dockerfiles/Manifests, and declarative **GitOps** synchronization engines like **ArgoCD** to manage cluster configurations without manual interventions.

---

## 🏗️ GitOps & CI/CD Pipeline Lifecycle

```
 ┌──────────┐      ┌──────────┐      ┌──────────┐      ┌──────────┐
 │  Commit  │ ───► │  Lint &  │ ───► │ Build &  │ ───► │ Security │
 │  to Git  │      │  Test    │      │ Compile  │      │  Scan    │
 └──────────┘      └──────────┘      └──────────┘      └──────────┘
                                                            │ Push Image
                                                            ▼
 ┌──────────┐      ┌──────────┐      ┌──────────┐      ┌──────────┐
 │ Target   │ ◄─── │  ArgoCD  │ ◄─── │ Config   │ ◄─── │  Docker  │
 │ K8s Pods │      │  Sync    │      │ Git Repo │      │ Registry │
 └──────────┘      └──────────┘      └──────────┘      └──────────┘
```

---

## 📘 Core Pipeline Concepts for AI Engineers

### 1. The GitOps Paradigm (ArgoCD)
With GitOps, Git is the single source of truth for all infrastructure. Instead of deploying applications manually using `kubectl apply`, you commit your Kubernetes manifests (or Helm charts) to a dedicated Git repository.
* **ArgoCD** runs as a controller inside the Kubernetes cluster. It continuously compares the running cluster state against the manifests declared in the Git repo.
* If a discrepancy is found (e.g., someone manually edits a service, or a developer updates a container tag in Git), ArgoCD automatically triggers a synchronization loop to align the cluster back to Git's state.

### 2. Container Linting & Security Scanning
* **Hadolint**: A linter that parses Dockerfiles and flags bad practices (like using `latest` tags, running as root, or missing package lockfiles).
* **Trivy**: A comprehensive security scanner that flags OS-level vulnerabilities (CVEs) and secret exposures within container images.

---

## 🛠️ Hands-on CI/CD Lab: GHA Workflow & ArgoCD Setup

In this lab, you will configure a complete, production-grade GitHub Actions pipeline that lints a Dockerfile, runs security scans, builds a Docker image, and structures an ArgoCD Application deployment.

### Step 1: Create a Production-Grade GitHub Actions Workflow
Create `.github/workflows/ci-cd.yml` in your repository:
```yaml
name: AI Platform CI/CD Pipeline

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  lint-and-audit:
    name: Lint & Security Audit
    runs-on: ubuntu-latest
    steps:
    # 1. Checkout Source Code
    - name: Checkout Code
      uses: actions/checkout@v3

    # 2. Lint Dockerfile using Hadolint
    - name: Lint Dockerfile
      uses: hadolint/hadolint-action@v3.1.0
      with:
        dockerfile: Dockerfile
        ignore: DL3008 # Ignore pin apt-get versions warning

    # 3. Lint Kubernetes Manifests
    - name: Lint K8s Manifests
      run: |
        sudo apt-get install -y yamllint
        yamllint -d relaxed kubernetes/

  build-and-scan:
    name: Build & Vulnerability Scan
    needs: lint-and-audit
    runs-on: ubuntu-latest
    steps:
    - name: Checkout Code
      uses: actions/checkout@v3

    # Set up QEMU for multi-arch builds (AMD64 and ARM64)
    - name: Set up QEMU
      uses: docker/setup-qemu-action@v2

    # Set up Docker Buildx for high-performance builds
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2

    # Build local image for scanning
    - name: Build local container image
      uses: docker/build-push-action@v4
      with:
        context: .
        load: true
        tags: ai-inference-app:local
        cache-from: type=gha
        cache-to: type=gha,mode=max

    # Run Trivy vulnerability scan
    - name: Scan Image for Vulnerabilities
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: 'ai-inference-app:local'
        format: 'table'
        exit-code: '1' # Fail the pipeline if HIGH or CRITICAL issues exist
        ignore-unfixed: true
        vuln-type: 'os,library'
        severity: 'CRITICAL,HIGH'
```

### Step 2: Create a Declarative ArgoCD Application Manifest
To deploy the built application automatically inside Kubernetes, declare this ArgoCD deployment manifest inside `kubernetes/argocd-app.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: ai-inference-platform
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.com
spec:
  project: default
  source:
    repoURL: 'https://github.com/hacrex/devops-ai-engineer-roadmap.git'
    targetRevision: HEAD
    path: kubernetes/overlays/production
    helm:
      valueFiles:
        - values.yaml
  destination:
    server: 'https://kubernetes.default.svc'
    namespace: ai-platform
  syncPolicy:
    automated:
      prune: true      # Automatically delete resources deleted in Git
      selfHeal: true   # Automatically revert changes made directly on cluster
    syncOptions:
      - CreateNamespace=true
      - ApplyOutOfSyncOnly=true
```

---

## 🔒 Security Considerations
1. **Runner Security**: Run your GitHub Actions workloads on private, self-hosted runners inside your own secure VPC when compiling enterprise code to prevent credential leakage.
2. **Cosign Signatures**: Use **Cosign** (Sigstore) in your pipelines to cryptographically sign built container images, ensuring the Kubernetes worker nodes reject unsigned images.
3. **Secrets Management**: Never write secrets to Git! Utilize a GitOps secrets controller like **Mozilla SOPS** or **HashiCorp Vault** to decrypt secrets dynamically in the cluster.

---

## 📈 Scaling & Observability Considerations
* **Docker Cache Tuning**: Use GitHub Actions Cache backends (`type=gha`) in your build steps. Deep learning container layers (containing PyTorch, CUDA, etc.) take 15 minutes to download; caching reduces build cycles to seconds.
* **Build Time Tracking**: Monitor deployment run times using GitHub dashboard integrations or Prometheus exporters targeting CI runners to spot slow pipeline components.

---

## 🔍 Troubleshooting Guide

### 💥 Issue: ArgoCD is Stuck in `OutOfSync` or `Degraded` State
* **Root Cause**: The Kubernetes manifest contains validation syntax errors, or physical cluster shortages (e.g. missing PVC volume) block resources from achieving healthy states.
* **Diagnostic Command**:
  ```bash
  # Check ArgoCD sync logs
  argocd app get ai-inference-platform --show-params
  ```
* **Mitigation**:
  1. Inspect the "Sync Result" panel in the ArgoCD UI to locate the invalid API or field name.
  2. Check target cluster logs using `kubectl describe` on the failing resource.
  3. Ensure target namespaces match the configurations specified in the ArgoCD application.

---

## 🌟 Best Practices & Open-Source Tools
* **ArgoCD Autopilot**: Use ArgoCD Autopilot to structure your GitOps repository directories automatically.
* **Renovate Bot**: Set up Renovate or Dependabot to automatically generate Pull Requests updating base images (`nvidia/cuda`) and Python package versions safely.
