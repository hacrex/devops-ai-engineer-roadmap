# 📚 DevOps AI Engineer Study Materials

Use this companion guide with [`ROADMAP.md`](./ROADMAP.md) when you want more depth, external references, and portfolio-building practice. The resources are grouped by learning phase so you can study one layer at a time instead of collecting random links.

> **How to use this file:** for each phase, read the official docs first, complete one hands-on lab, then summarize what you learned in your own runbook or GitHub project README.

---

## 🎯 Study Strategy

| Cadence | What to do | Output |
| :--- | :--- | :--- |
| Daily | Spend 45-90 minutes reading one focused topic and taking notes. | One page of notes or a small code/config snippet. |
| Weekly | Build one small lab tied to the current phase. | A reproducible README with commands, screenshots, and troubleshooting notes. |
| Biweekly | Convert the lab into a portfolio artifact. | A GitHub project, diagram, blog post, or recorded demo. |
| Monthly | Review security, reliability, and cost tradeoffs. | A short architecture decision record (ADR). |

---

## 🧱 Phase 1: Linux, Containers, Networking, and IaC

### Core resources

| Topic | Resource | Why it matters |
| :--- | :--- | :--- |
| Linux systems | [The Linux Documentation Project](https://tldp.org/) | Builds command-line, filesystem, shell, and networking fundamentals. |
| Linux performance | [Brendan Gregg's Linux Performance materials](https://www.brendangregg.com/linuxperf.html) | Helps you reason about CPU, memory, disk, and network bottlenecks. |
| Containers | [Docker Docs](https://docs.docker.com/) | Covers images, Compose, build cache, networking, volumes, and production concerns. |
| Kubernetes basics | [Kubernetes Concepts](https://kubernetes.io/docs/concepts/) | Establishes Pods, Services, workloads, storage, config, and security models. |
| Terraform | [Terraform Language Documentation](https://developer.hashicorp.com/terraform/language) | Teaches repeatable infrastructure definitions, modules, variables, and state. |

### Practice labs

- Recreate a minimal container runtime demo with Linux namespaces and cgroups.
- Build a multi-stage Dockerfile for a Python API and run it as a non-root user.
- Provision a small VM or Kubernetes cluster using Terraform and document teardown steps.

---

## ☸️ Phase 2: Kubernetes Platform Engineering

### Core resources

| Topic | Resource | Why it matters |
| :--- | :--- | :--- |
| Workloads | [Kubernetes Workloads](https://kubernetes.io/docs/concepts/workloads/) | Explains Deployments, Jobs, DaemonSets, and workload lifecycle patterns. |
| Services and networking | [Kubernetes Services, Load Balancing, and Networking](https://kubernetes.io/docs/concepts/services-networking/) | Needed for service discovery, ingress, traffic routing, and cluster connectivity. |
| Storage | [Kubernetes Storage](https://kubernetes.io/docs/concepts/storage/) | Covers persistent volumes, storage classes, CSI, and stateful workloads. |
| Security | [Kubernetes Security Concepts](https://kubernetes.io/docs/concepts/security/) | Introduces RBAC, admission control, secrets, policies, and hardening. |
| Observability | [Kubernetes Observability](https://kubernetes.io/docs/concepts/cluster-administration/observability/) | Connects metrics, logs, traces, and operational automation. |

### Practice labs

- Deploy a three-tier app with ConfigMaps, Secrets, Services, readiness probes, and resource limits.
- Add NetworkPolicies and RBAC roles to restrict access between namespaces.
- Create a troubleshooting runbook for `CrashLoopBackOff`, image pull errors, and pending Pods.

---

## 🧠 Phase 3: Local LLMs, Inference, and GPU Foundations

### Core resources

| Topic | Resource | Why it matters |
| :--- | :--- | :--- |
| Local model serving | [Ollama Documentation](https://github.com/ollama/ollama/tree/main/docs) | Useful for quick local model serving, model pulls, and API experimentation. |
| CPU/GPU model runtime | [llama.cpp Documentation](https://github.com/ggml-org/llama.cpp) | Teaches GGUF model execution, quantization, benchmarking, and local inference constraints. |
| GPU software stack | [NVIDIA CUDA Toolkit Documentation](https://docs.nvidia.com/cuda/) | Provides the base concepts behind CUDA-enabled workloads and GPU programming constraints. |
| Kubernetes GPUs | [NVIDIA GPU Operator Documentation](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/index.html) | Shows how drivers, device plugins, monitoring, and runtime integration are managed in Kubernetes. |
| High-throughput serving | [vLLM Documentation](https://docs.vllm.ai/) | Covers OpenAI-compatible serving, batching, memory management, and inference deployment. |

### Practice labs

- Benchmark the same prompt on CPU-only, quantized, and GPU-backed runtimes.
- Run an OpenAI-compatible vLLM server and test it with a simple HTTP client.
- Write a GPU sizing note comparing context length, model size, quantization, and throughput.

---

## 🔎 Phase 4: RAG, Embeddings, and Vector Databases

### Core resources

| Topic | Resource | Why it matters |
| :--- | :--- | :--- |
| Embeddings and datasets | [Hugging Face Course](https://huggingface.co/learn) | Gives practical grounding in transformers, tokenizers, datasets, and model workflows. |
| Vector database | [Qdrant Documentation](https://qdrant.tech/documentation/) | Explains collections, payloads, filtering, HNSW indexes, backups, and production operations. |
| PostgreSQL vectors | [pgvector README](https://github.com/pgvector/pgvector) | Useful for teams standardizing retrieval inside PostgreSQL. |
| RAG evaluation | [Ragas Documentation](https://docs.ragas.io/) | Helps measure context precision, faithfulness, and answer quality. |
| Search basics | [Elasticsearch Relevance documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-filter-context.html) | Helps you compare lexical, vector, and hybrid retrieval tradeoffs. |

### Practice labs

- Build an ingestion pipeline with chunking, metadata, embedding generation, and idempotent upserts.
- Compare Qdrant vector-only search with Postgres `pgvector` for the same document set.
- Add a small evaluation dataset and measure retrieval quality before changing chunk size.

---

## 🤖 Phase 5: Agents, Tools, MCP, and Automation

### Core resources

| Topic | Resource | Why it matters |
| :--- | :--- | :--- |
| Agent/tool protocol | [Model Context Protocol Documentation](https://modelcontextprotocol.io/docs) | Defines a standard way to connect models to tools, context, and external systems. |
| Workflow automation | [n8n Documentation](https://docs.n8n.io/) | Useful for event-driven operations, approvals, and API workflows. |
| Agent frameworks | [LangChain Documentation](https://python.langchain.com/docs/) | Common reference for tool calling, retrieval, and agent orchestration patterns. |
| LLM app evaluation | [OpenAI Evals](https://github.com/openai/evals) | Shows how to structure repeatable model and prompt evaluation tasks. |
| Structured configs | [Pydantic Documentation](https://docs.pydantic.dev/) | Helps validate tool inputs, model outputs, and automation configuration. |

### Practice labs

- Build a read-only Kubernetes diagnostic tool that summarizes Pod status and events.
- Create an MCP server that exposes safe filesystem or cluster-inspection actions.
- Add an approval gate before any agent can run a mutating infrastructure command.

---

## 📈 Phase 6: Observability, AIOps, Security, and Governance

### Core resources

| Topic | Resource | Why it matters |
| :--- | :--- | :--- |
| Telemetry standard | [OpenTelemetry Documentation](https://opentelemetry.io/docs/) | Establishes vendor-neutral traces, metrics, logs, context propagation, and instrumentation. |
| Metrics and alerting | [Prometheus Documentation](https://prometheus.io/docs/introduction/overview/) | Covers scraping, PromQL, alerting, and service-level indicators. |
| Dashboards | [Grafana Documentation](https://grafana.com/docs/) | Helps turn metrics, logs, and traces into operational views. |
| LLM observability | [Langfuse Documentation](https://langfuse.com/docs) | Adds tracing, prompt/version tracking, evaluations, and feedback loops for LLM apps. |
| LLM security | [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) | Frames prompt injection, insecure output handling, supply chain, data leakage, and agent risks. |
| AI risk management | [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) | Gives governance language for mapping, measuring, managing, and documenting AI risk. |

### Practice labs

- Instrument an LLM API with request latency, token usage, model errors, and cost metrics.
- Create alerts for high error rates, slow inference, vector database failures, and GPU saturation.
- Threat-model a RAG app using OWASP LLM risks and write mitigations for each major risk.

---

## 🧪 Portfolio Project Ideas

| Level | Project | What to demonstrate |
| :--- | :--- | :--- |
| Beginner | Local AI DevOps Copilot | Prompt design, local model calls, structured output, YAML validation. |
| Intermediate | RAG Runbook Assistant | Ingestion, embeddings, vector search, citations, evaluation, Docker Compose. |
| Intermediate | AI Log Analyzer | FastAPI, Vector/Fluent Bit, alert routing, LLM diagnosis, fallback mode. |
| Advanced | Kubernetes Inference Platform | GPU Operator, vLLM, autoscaling, ingress, secrets, dashboards, runbooks. |
| Advanced | Safe SRE Agent | Tool permissions, approval gates, rollback strategy, audit logs, incident timeline. |

---

## ✅ Study Milestones

- [ ] I can explain how containers use namespaces, cgroups, and layered filesystems.
- [ ] I can debug a failing Kubernetes workload using events, logs, probes, and resource metrics.
- [ ] I can run and benchmark a local LLM with at least two runtime configurations.
- [ ] I can design a RAG pipeline with chunking, metadata, retrieval, and evaluation.
- [ ] I can deploy an OpenAI-compatible inference endpoint and monitor latency, tokens, and errors.
- [ ] I can describe the main OWASP LLM risks and map controls to my AI platform.
- [ ] I can build a safe automation agent with restricted tools, approval steps, and auditability.

---

## 🧭 Recommended Order for Beginners

1. [`QUICKSTART.md`](./QUICKSTART.md) for the fastest hands-on entry point.
2. [`HOME_LAB_REQUIREMENTS.md`](./HOME_LAB_REQUIREMENTS.md) to choose local hardware, cloud APIs, NVIDIA NIM, or Hugging Face.
3. [`AI_ECOSYSTEM.md`](./AI_ECOSYSTEM.md) to track llmfit, llm-checker, AI companies, and model families.
4. [`ROADMAP.md`](./ROADMAP.md) for the 24-week progression.
5. [`12-days-series/README.md`](./12-days-series/README.md) for daily labs.
6. This study guide for deeper reading and extra projects.
7. [`projects/`](./projects/) for portfolio-level implementation practice.
