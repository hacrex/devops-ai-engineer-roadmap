# 📈 DevOps AI Engineer Learning Roadmap

Transitioning from a traditional DevOps, Platform, or SRE engineer to an **AI Infrastructure & Platform Engineer** requires a deep understanding of hardware virtualization, high-throughput container networking, GPU resource orchestration, distributed inference, model security, and agentic workflows. 

This roadmap is divided into **6 progressive phases** across a suggested 24-week timeline.

---

## 🗺️ High-Level Learning Path

```
  ┌────────────────────────────────────────────────────────┐
  │         Phase 1: Bare-Metal & Cloud Foundations         │
  │     Linux kernel internals, cgroups v2, Rook/Ceph, IaC  │  (Weeks 1-4)
  └───────────────────────────┬────────────────────────────┘
                              ▼
  ┌────────────────────────────────────────────────────────┐
  │       Phase 2: Local Model Runtimes & Optimization     │
  │     Ollama, llama.cpp, quantization, GPU architecture  │  (Weeks 5-8)
  └───────────────────────────┬────────────────────────────┘
                              ▼
  ┌────────────────────────────────────────────────────────┐
  │        Phase 3: Prompting, MCP, & Agent Workflows      │
  │   System instructions, tools, Custom Python MCP, n8n   │  (Weeks 9-12)
  └───────────────────────────┬────────────────────────────┘
                              ▼
  ┌────────────────────────────────────────────────────────┐
  │       Phase 4: Cloud-Native Kubernetes AI Engines      │
  │    NVIDIA Operator, MIG, vLLM, KServe, KEDA Scaling    │  (Weeks 13-16)
  └───────────────────────────┬────────────────────────────┘
                              ▼
  ┌────────────────────────────────────────────────────────┐
  │        Phase 5: High-Speed Storage & Vector RAG        │
  │  Chunking strategy, Qdrant cluster, hybrid search, pg  │  (Weeks 17-20)
  └───────────────────────────┬────────────────────────────┘
                              ▼
  ┌────────────────────────────────────────────────────────┐
  │        Phase 6: Enterprise AIOps, Observability & Sec   │
  │    OpenLIT, Langfuse, Guardrails, OWASP security, SRE  │  (Weeks 21-24)
  └────────────────────────────────────────────────────────┘
```

---

## 📚 Phase-by-Phase Roadmap Details

---

### Phase 1: Bare-Metal & Cloud Foundations (Weeks 1-4)
* **Goal**: Master system-level resource virtualization, high-speed networking, and programmatic infrastructure provisioning.
* **Topics**:
  * **Linux Internals**: cgroups v2 (CPU/Memory isolation), namespaces (network, pid, mount, ipc), eBPF.
  * **Networking**: veth pairs, iptables routing, CoreDNS, container interfaces (CNI), Envoy proxies.
  * **Storage**: High-throughput distributed storage (Rook/Ceph, MinIO), CSI drivers, host-path local volumes.
  * **Infrastructure as Code**: Terraform modules for GPU-enabled GCP/AWS virtual machines.
* **Hands-on Checklist**:
  - [ ] Write a custom bash script that creates a Linux network namespace, configures veth pairs, and routes internet traffic to it manually using iptables.
  - [ ] Deploy a local Kubernetes cluster (Kind) and install the local-path storage provisioner.
  - [ ] Write a Terraform manifest to spin up an EC2 instance with NVIDIA L4 drivers preloaded using cloud-init.
* **Recommended Learning Reference**: [Fundamentals Module](./fundamentals/)

---

### Phase 2: Local Model Runtimes & Optimization (Weeks 5-8)
* **Goal**: Understand GPU architecture, host drivers, local model execution runtimes, and parameter compression (quantization).
* **Topics**:
  * **GPU Architecture**: CUDA cores, Tensor cores, HBM (High Bandwidth Memory), PCI-e bandwidth vs. NVLink, vRAM budget mapping.
  * **Runtimes**: llama.cpp (GGUF CPU execution), Ollama API serving, OpenWebUI.
  * **Quantization**: Mathematical concepts behind GGUF, AWQ, EXL2. Int4, Int8, and FP16 precision comparison.
* **Hands-on Checklist**:
  - [ ] Run llama.cpp CLI to compile a GGUF model and run a benchmark test measuring Token-per-Second (T/S) on CPU.
  - [ ] Deploy Ollama and OpenWebUI in Docker Compose with CUDA acceleration.
  - [ ] Create a custom `Modelfile` with tailored system prompts, parameters (temperature, top_p), and system constraints.
* **Recommended Learning Reference**: [Local LLMs Module](./local-llms/)

---

### Phase 3: Prompting, MCP, & Agent Workflows (Weeks 9-12)
* **Goal**: Programmatically bridge LLMs with operational tools and infrastructure APIs using standard protocols.
* **Topics**:
  * **Prompting Paradigms**: System instructions, Chain-of-Thought (CoT), Few-Shot, ReAct (Reasoning and Acting).
  * **Model Context Protocol (MCP)**: JSON-RPC communication structure, MCP client-server loop, context orchestration.
  * **Agentic Frameworks**: Multi-agent cooperation, Tool Calling, autonomous task delegation.
  * **Orchestration Tools**: Event-driven automation using n8n and sim.io workflow engines.
* **Hands-on Checklist**:
  - [ ] Write a custom Python MCP Server that exposes local tools (e.g., executing commands, reading Kubernetes cluster status) to Claude or Copilot.
  - [ ] Build an n8n webhook flow that triggers an LLM review when a new Git Pull Request is opened.
  - [ ] Design a `skills.md` instruction set that forces an autonomous coding agent to write linted, secure Go code.
* **Recommended Learning Reference**: [Prompt Engineering](./prompt-engineering/), [MCP](./mcp/), [Skills.md](./skills-md/), [Orchestration](./orchestration/)

---

### Phase 4: Cloud-Native Kubernetes AI Engines (Weeks 13-16)
* **Goal**: Architect high-availability, auto-scaling model serving architectures on Kubernetes clusters.
* **Topics**:
  * **GPU Scheduling**: NVIDIA GPU Operator, fractional GPU allocation, Multi-Instance GPU (MIG) slicing, Karpenter node provisioning.
  * **Serving Engines**: vLLM distributed engine, KServe Custom Predictors, Ray Serve cluster configurations.
  * **Autoscaling**: KEDA (Kubernetes Event-driven Autoscaling) queue-length scaling, HPA custom metrics.
* **Hands-on Checklist**:
  - [ ] Install the NVIDIA GPU Operator via Helm on a Kubernetes cluster.
  - [ ] Deploy a vLLM engine serving a Llama-3 model using an Ingress Gateway (e.g., Istio or Traefik) and configure JWT authentication.
  - [ ] Set up KEDA to scale vLLM pods from 1 to N based on the `vllm:num_requests_waiting` Prometheus metric.
* **Recommended Learning Reference**: [Kubernetes AI Module](./kubernetes-ai/)

---

### Phase 5: High-Speed Storage & Vector RAG (Weeks 17-20)
* **Goal**: Build and scale Retrieval-Augmented Generation (RAG) platforms using high-performance vector databases.
* **Topics**:
  * **RAG Architectures**: Chunking strategies (semantic, sliding window), embedding algorithms (sentence-transformers), rerankers.
  * **Vector Databases**: Qdrant cluster architecture, ChromaDB persistent storage, pgvector indexing (HNSW, IVFFlat).
  * **Platform Integration**: High-availability database replication, backup strategies, and fast-index query optimization.
* **Hands-on Checklist**:
  - [ ] Build a Python ingestion pipeline that parses PDF files, chunks them semantically, and upserts vectors into Qdrant.
  - [ ] Deploy Qdrant in a distributed, clustered configuration on Kubernetes with persistent volume claims.
  - [ ] Write a Postgres SQL script to create a pgvector column, insert high-dimensional embeddings, and run HNSW indexing queries.
* **Recommended Learning Reference**: [RAG & Vector DB Module](./rag-vector-db/)

---

### Phase 6: Enterprise AIOps, Observability & Security (Weeks 21-24)
* **Goal**: Establish enterprise guardrails, log-tracing observability, threat prevention, and self-healing SRE automations.
* **Topics**:
  * **AI Observability**: OpenTelemetry semantic conventions, Langfuse request tracing, OpenLIT metrics scraping.
  * **Security & Governance**: OWASP Top 10 LLM vulnerabilities, Prompt Injection detection, Llama Guard scanning, secure container networks.
  * **AIOps & Auto-Healing**: Event log vectorization, Alertmanager automations, SRE diagnostics pipelines.
* **Hands-on Checklist**:
  - [ ] Implement OpenLIT to collect distributed traces from a vLLM serving container and visualize them on a Grafana Dashboard.
  - [ ] Configure LlamaGuard as an API gateway proxy to scan incoming requests and outgoing model completions for malicious instructions.
  - [ ] Create an AI SRE Agent that automatically listens to Kubernetes pod crash alerts, analyzes logs with a local LLM, and triggers healing actions.
* **Recommended Learning Reference**: [Observability](./observability-aiops/), [AI Security](./ai-security/), [AI SRE Capstone](./projects/ai-sre-agent/)

---

## 🏆 Graduation Checkpoint

By completing all phases and executing the **Capstone Projects**, you will have built a comprehensive personal portfolio demonstrating deep expertise in building cloud-native AI platforms. You will be fully equipped to design, deploy, and scale enterprise AI systems securely and cost-effectively!
