# 📅 12-Day DevOps to AI Infrastructure Engineer Challenge

Welcome to the **12-Day DevOps to AI Infrastructure Engineer Learning Series**! This structured guide compiles daily high-impact playbooks, visual architectures, actionable lab playbooks, and content templates to help you master AI platform engineering.

Use these daily summaries to guide your daily studies or to draft social posts detailing your learning journey!

---

## 🗺️ The 12-Day Curriculum Matrix

| Day | Focus Topic | Key Practical Takeaway | Curriculum Reference |
| :--- | :--- | :--- | :--- |
| **Day 1** | **Linux & Containers** | Optimize static hugepages & write PyTorch GPU Dockerfile. | [Linux & Containers](../fundamentals/linux-fundamentals.md) |
| **Day 2** | **Kubernetes Basics** | Deploy InitContainers to pull weights dynamically before boot. | [Kubernetes Storage](../fundamentals/storage.md) |
| **Day 3** | **Python Automation** | Build a pod diagnostics CLI wrapper using `kubernetes-client`. | [Python Automation](../fundamentals/python-automation.md) |
| **Day 4** | **Prompt Engineering** | Compile strict JSON Schemas for AI model Tool Calling. | [Prompt Engineering](../prompt-engineering/README.md) |
| **Day 5** | **Local LLM Serving** | Size GPU VRAM math and serve models locally via Ollama. | [Local LLMs](../local-llms/README.md) |
| **Day 6** | **Hugging Face Hub** | Programmatically verify Safetensors files and clear model caches. | [Hugging Face](../huggingface/README.md) |
| **Day 7** | **Inference in K8s** | Serve LLMs via vLLM and autoscaled replicas with KEDA. | [Kubernetes AI](../kubernetes-ai/README.md) |
| **Day 8** | **AI Agents & MCP** | Build a Model Context Protocol (MCP) server for systems control. | [MCP & Agents](../mcp/README.md) |
| **Day 9** | **RAG & Vector DBs** | Ingest operational runbooks and run similarity queries in Qdrant. | [RAG & Vector DBs](../rag-vector-db/README.md) |
| **Day 10** | **AI Observability** | Trace LLM completion spans and export telemetry with OpenLIT. | [Observability](../observability-aiops/README.md) |
| **Day 11** | **AI Guardrails & Security** | Build a FastAPI gatekeeper and write ingress NetworkPolicies. | [AI Security](../ai-security/README.md) |
| **Day 12** | **Real-world Capstones** | Deploy RAG web apps, SRE webhook healers, and GKE GPU pools. | [Capstone Projects](../projects/local-rag-assistant/README.md) |

---

## 📝 Day 1: Linux Internals, cgroups v2, and Container GPU Runtimes

### 🧠 Core Concepts
Traditional CPU metrics fail to describe LLM memory allocations. DevOps engineers must understand Linux process state transitions, cgroups v2 boundaries, virtual memory transparent hugepages, and the **NVIDIA Container Runtime** driver layer.

```
 ┌────────────────────────┐
 │ Container Host OS      │
 │  cgroups v2 & Hugepages│
 └───────────┬────────────┘
             │ Intercepts GPU calls
             ▼
 ┌────────────────────────┐
 │ NVIDIA Container Toolkit│
 │  nvidia-container-cli  │
 └───────────┬────────────┘
             │ Mounts kernel drivers (/dev/nvidia*)
             ▼
 ┌────────────────────────┐
 │ GPU Inference Container│
 │  CUDA / PyTorch / vLLM │
 └────────────────────────┘
```

### ⚡ Practical Playbook: Allocate Static Hugepages
Reserve high-speed 2MB hugepages to reduce memory translation overhead during large weight loadings:
```bash
# Verify available hugepage allocation configurations
grep Huge /proc/meminfo

# Dynamically allocate 1024 hugepages of 2MB each
sudo sysctl -w vm.nr_hugepages=1024
```

---

## 📝 Day 2: Kubernetes Control Plane & CSI Weight-Load Latency

### 🧠 Core Concepts
Weights for a 7-Billion parameter model exceed 14GB on disk. Using standard NFS volumes introduces unacceptable cold-start latencies. AI Platform engineers utilize specialized Local Path Provisioners or high-performance NVMe CSI drivers to enable zero-copy memory mapping.

### ⚡ Practical Playbook: Helm-Driven GPU Operator Setup
Deploy NVIDIA's official operator to auto-inject GPU hardware parameters:
```bash
helm repo add nvidia https://helm.github.io/gpu-operator
helm repo update
helm install gpu-operator nvidia/gpu-operator -n gpu-operator --create-namespace
```

---

## 📝 Day 3: Custom Python SDK Diagnostics Automation

### 🧠 Core Concepts
Parsing JSON logs manually slows recovery times. Writing dedicated Python CLI scripts using the official `kubernetes` SDK enables instant automation to describe failing pods, read error states, and automate pod remediation.

### ⚡ Practical Playbook: Programmatic Pod Diagnostic Script
```python
from kubernetes import client, config

config.load_kube_config()
v1 = client.CoreV1Api()

# Find failing pods in default namespace
pods = v1.list_namespaced_pod(namespace="default")
for pod in pods.items:
    if pod.status.phase != "Running":
        print(f"🚨 Pod '{pod.metadata.name}' is in status: '{pod.status.phase}'")
```

---

## 📝 Day 4: Prompt Engineering & System Tool Calling APIs

### 🧠 Core Concepts
To allow models to interact with real systems (like restarting a service), we must convert model natural language outputs into strict JSON schemas. **Structured Outputs** bind system APIs to models seamlessly.

### ⚡ Practical Playbook: Tool Calling JSON Schema
Define the target structure for an API restart tool:
```json
{
  "name": "restart_service",
  "description": "Triggers a rolling restart on a target Kubernetes deployment.",
  "parameters": {
    "type": "object",
    "properties": {
      "deployment_name": {"type": "string"},
      "namespace": {"type": "string", "default": "default"}
    },
    "required": ["deployment_name"]
  }
}
```

---

## 📝 Day 5: Local LLMs, quantized weights, and vRAM Calculations

### 🧠 Core Concepts
Before deploying models, you must calculate precise VRAM sizing to prevent GPU Out Of Memory (OOM) failures. Quantization formats (GGUF, AWQ, GPTQ) compress floating-point weights to run on smaller cards.

### 🧮 VRAM Math
$$\text{Total VRAM} = \left( \frac{\text{Parameter Count} \times \text{Bit Quantization}}{8} \right) \times 1.25\text{ overhead multiplier} + \text{KV Cache allocation}$$

### ⚡ Practical Playbook: Deploy Local Ollama Node
```bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
docker exec -it ollama ollama run qwen2.5-coder:7b
```

---

## 📝 Day 6: Hugging Face Ecosystem, CLI Caching & Safetensors

### 🧠 Core Concepts
PyTorch's default `.bin` files are based on `pickle` serialization, allowing arbitrary code execution vulnerabilities during download. Modern enterprise environments enforce the zero-copy, secure **Safetensors** file format.

### ⚡ Practical Playbook: HF CLI Model Cache Prune
Clear duplicate cached weights from disk:
```bash
# Check Hugging Face download caching folders
huggingface-cli env

# Interactively scan and prune model caches
huggingface-cli delete-cache
```

---

## 📝 Day 7: AI Inference Serving in Kubernetes: vLLM & KEDA

### 🧠 Core Concepts
Standard CPU/RAM metrics are useless for autoscaling model serving containers. Auto-remediating platforms must scale replicas up and down exclusively based on Prometheus exporters reading active request queues (e.g. `vllm:num_requests_waiting`).

```
 ┌───────────────┐ High pending queues  ┌───────────────┐  Scales pods 1 to 5  ┌──────────────┐
 │ vLLM Exporter │ ───────────────────► │ Prometheus DB │ ──────────────────► │ KEDA HPA     │
 └───────────────┘                      └───────────────┘                      └──────────────┘
```

### ⚡ Practical Playbook: KEDA Metric Scale Manifest
```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: vllm-scaler
  namespace: ai-platform
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: vllm-inference-deployment
  triggers:
  - type: prometheus
    metadata:
      serverAddress: http://prometheus:9090
      metricName: vllm_num_requests_waiting
      query: sum(vllm:num_requests_waiting)
      threshold: '5'
```

---

## 📝 Day 8: Autonomous SRE Agents & Model Context Protocol (MCP)

### 🧠 Core Concepts
The Model Context Protocol (MCP) by Anthropic is an open-standard JSON-RPC protocol over stdin/stdout or SSE transport layers to expose **Tools, Prompts, and Resources** to AI clients.

### ⚡ Practical Playbook: FastMCP Server Lab
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("infra-tools")

@mcp.tool()
def reboot_system(node_name: str) -> str:
    """Safely issues a reboot annotation on a target node."""
    return f"🔧 Reboot instruction compiled for '{node_name}'."

if __name__ == "__main__":
    mcp.run()
```

---

## 📝 Day 9: RAG & High-Performance Vector Databases

### 🧠 Core Concepts
Retrieval-Augmented Generation (RAG) resolves training cutoff limitations. High-performance vector databases (such as **Qdrant**) index mathematical text representations (embeddings) using hierarchical graphs (HNSW) to achieve sub-millisecond search latencies.

### ⚡ Practical Playbook: Python Qdrant Search Ingestion
```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient(":memory:")
client.create_collection(
    collection_name="runbooks",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)
print("🟢 Vector Collection initialized.")
```

---

## 📝 Day 10: AI Observability & Distributed Tracing

### 🧠 Core Concepts
Monitoring standard HTTP response codes is not enough. You must track Time-to-First-Token (TTFT), Inter-Token Latency (ITL), token usage costs, and full span maps using **OpenTelemetry**, **Langfuse**, and **OpenLIT**.

### ⚡ Practical Playbook: Instrumented Telemetry Exporter
```python
import openlit

openlit.init(
    application_name="ai-sre-copilot",
    environment="production"
)
print("📊 AI telemetry trace exporter active.")
```

---

## 📝 Day 11: AI Security, Prompt Injection & Llama Guard

### 🧠 Core Concepts
Integrating AI into enterprise systems opens up new vulnerabilities. Prompt injection (jailbreaking) attempts to bypass system constraints. Guardrails like **Llama Guard** classify prompt input safety.

### ⚡ Practical Playbook: FastAPI Safety Gatekeeper Proxy
```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.post("/chat")
def chat(prompt: str):
    if "ignore instructions" in prompt.lower():
        raise HTTPException(status_code=403, detail="Threat: Prompt injection blocked.")
    return {"status": "Safe"}
```

---

## 📝 Day 12: Real-World AI Infrastructure Projects

### 🧠 Core Concepts
Combine the entire curriculum into deployable systems! Review our 5 Capstone Projects in the roadmap to build and deploy:
1. **Local RAG Assistant**: Streamlit dashboard + Qdrant DB.
2. **AI DevOps Copilot**: Local YAML/HCL CLI generator.
3. **AI Log Analysis Pipeline**: Event-driven Vector syslog routing + LLM classification.
4. **Kubernetes AI Platform**: GKE GPU terraform modules + KServe.
5. **AI SRE Agent**: Automated self-healing alerts + rolling deployment restarts.

Let's apply these lessons to build enterprise-grade, reliable AI platforms!
