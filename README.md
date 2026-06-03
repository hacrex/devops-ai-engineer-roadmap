# 🚀 DevOps AI Engineer Roadmap

[![Platform](https://img.shields.io/badge/Platform-Kubernetes%20%7C%20Docker%20%7C%20Cloud-blue?style=for-the-badge&logo=kubernetes)](https://kubernetes.io)
[![AI Stack](https://img.shields.io/badge/AI-vLLM%20%7C%20Ollama%20%7C%20RAG-orange?style=for-the-badge)](./STUDY_MATERIALS.md)
[![Projects](https://img.shields.io/badge/Hands--on-5%20Capstone%20Projects-green?style=for-the-badge)](./projects/)
[![License](https://img.shields.io/badge/License-MIT-red?style=for-the-badge)](./LICENSE)

A practical, project-first roadmap for DevOps, Platform, SRE, and Cloud engineers who want to become **AI Infrastructure / AI Platform Engineers**.

This repository connects traditional infrastructure skills—Linux, containers, Kubernetes, Terraform, CI/CD, observability, and security—with the modern AI platform stack: local LLMs, GPU scheduling, inference serving, RAG systems, agents, MCP, and AI safety.

---

## 📌 Table of Contents

- [Who This Is For](#-who-this-is-for)
- [What You Will Build](#-what-you-will-build)
- [Repository Map](#-repository-map)
- [Recommended Learning Paths](#-recommended-learning-paths)
- [Core Curriculum](#-core-curriculum)
- [Capstone Projects](#-capstone-projects)
- [Quick Start](#-quick-start)
- [Suggested Improvements for This Repo](#-suggested-improvements-for-this-repo)
- [Contributing](#-contributing)

---

## 👤 Who This Is For

This roadmap is designed for learners who already know at least one of these areas and want to move toward AI platform work:

- **DevOps engineers** who want to deploy and operate LLM-powered systems.
- **SREs** who want to build AI-assisted observability, alerting, and remediation workflows.
- **Platform engineers** who want to run GPU-backed inference platforms on Kubernetes.
- **Cloud engineers** who want to provision AI-ready infrastructure using Terraform and Kubernetes.
- **Backend engineers** who want to understand RAG, model serving, and production AI operations.

If you are new to DevOps, start with the [Fundamentals](./fundamentals/) modules and the [12 Days Series](./12-days-series/README.md) before jumping into the advanced projects.

---

## 🧪 What You Will Build

By following this repository, you will practice building:

- Local LLM runtimes with Ollama and llama.cpp-style workflows.
- Secure Kubernetes manifests for AI workloads.
- RAG pipelines with vector databases and local inference.
- AI-assisted log analysis and incident triage services.
- GPU-aware Kubernetes inference platforms with autoscaling.
- Agentic DevOps tools that interact with infrastructure safely.
- Observability and guardrail patterns for LLM applications.

---

## 🗂️ Repository Map

| Path | Purpose |
| :--- | :--- |
| [`ROADMAP.md`](./ROADMAP.md) | 24-week phased roadmap from infrastructure fundamentals to AI security and AIOps. |
| [`QUICKSTART.md`](./QUICKSTART.md) | Fastest path to run a local lab and start building. |
| [`STUDY_MATERIALS.md`](./STUDY_MATERIALS.md) | Curated study resources, official docs, labs, portfolio ideas, and milestones. |
| [`HOME_LAB_REQUIREMENTS.md`](./HOME_LAB_REQUIREMENTS.md) | Hardware tiers, local LLM sizing, cloud API options, NVIDIA NIM, and Hugging Face setup. |
| [`AI_ECOSYSTEM.md`](./AI_ECOSYSTEM.md) | llmfit, llm-checker, top AI companies to track, model families, and model-selection guidance. |
| [`12-days-series/`](./12-days-series/README.md) | Daily hands-on learning sequence for core DevOps + AI skills. |
| [`fundamentals/`](./fundamentals/) | Linux, networking, Docker, Kubernetes, CI/CD, Terraform, storage, and Python automation notes. |
| [`prompt-engineering/`](./prompt-engineering/) | Prompting patterns, structured outputs, tool use, and evaluation concepts. |
| [`local-llms/`](./local-llms/) | Local model runtimes, model formats, quantization, and performance tuning. |
| [`kubernetes-ai/`](./kubernetes-ai/) | GPU Operator, inference serving, KServe, vLLM, KEDA, and Kubernetes AI operations. |
| [`rag-vector-db/`](./rag-vector-db/) | Retrieval-augmented generation, embeddings, Qdrant, ChromaDB, pgvector, and vector search. |
| [`ai-agents/`](./ai-agents/) | Agent design, tool calling, safe automation, and multi-agent workflows. |
| [`mcp/`](./mcp/) | Model Context Protocol concepts and server patterns. |
| [`observability-aiops/`](./observability-aiops/) | OpenTelemetry, AI tracing, logs, metrics, and incident automation. |
| [`ai-security/`](./ai-security/) | Prompt injection, guardrails, secrets, network policy, and LLM security risks. |
| [`projects/`](./projects/) | Portfolio-grade capstone projects and runnable examples. |
| [`diagrams/`](./diagrams/README.md) | Mermaid architecture diagrams and rendering instructions. |

---

## 🧭 Recommended Learning Paths

### 🟢 Beginner: DevOps to AI Foundations

1. Read [`QUICKSTART.md`](./QUICKSTART.md).
2. Complete [`12-days-series/day01-linux-containers`](./12-days-series/day01-linux-containers/).
3. Complete the Kubernetes and Python automation days in [`12-days-series/`](./12-days-series/README.md).
4. Read [`local-llms/`](./local-llms/) and run one local model.
5. Build the [`AI DevOps Copilot`](./projects/ai-devops-copilot/) project.

### 🟡 Intermediate: Platform Engineer to AI Platform Engineer

1. Review [`fundamentals/kubernetes-basics.md`](./fundamentals/kubernetes-basics.md) and [`fundamentals/terraform.md`](./fundamentals/terraform.md).
2. Study [`kubernetes-ai/`](./kubernetes-ai/) and [`local-llms/`](./local-llms/).
3. Build the [`Local RAG Assistant`](./projects/local-rag-assistant/).
4. Deploy the [`Kubernetes AI Platform`](./projects/kubernetes-ai-platform/).
5. Add observability from [`observability-aiops/`](./observability-aiops/).

### 🔴 Advanced: SRE / AIOps / Security Specialist

1. Study [`ai-agents/`](./ai-agents/), [`mcp/`](./mcp/), and [`ai-security/`](./ai-security/).
2. Build the [`AI Log Analysis Pipeline`](./projects/ai-log-analysis-pipeline/).
3. Build the [`AI SRE Agent`](./projects/ai-sre-agent/).
4. Add approval gates, audit logs, and rollback controls.
5. Document security tradeoffs using [`STUDY_MATERIALS.md`](./STUDY_MATERIALS.md).

---

## 🧱 Core Curriculum

| Module | Topic | Key Outcomes |
| :--- | :--- | :--- |
| 1 | [Fundamentals](./fundamentals/) | Linux, networking, Docker, Kubernetes basics, CI/CD, Terraform, storage, and automation. |
| 2 | [Prompt Engineering](./prompt-engineering/) | Prompt patterns, context management, structured outputs, tool calls, and evaluations. |
| 3 | [Local LLMs](./local-llms/) | Ollama, model formats, quantization, local inference, and CPU/GPU tradeoffs. |
| 4 | [Hugging Face](./huggingface/) | Transformers, datasets, model registries, tokenizers, and model workflows. |
| 5 | [Kubernetes AI](./kubernetes-ai/) | GPU scheduling, NVIDIA GPU Operator, vLLM, KServe, KEDA, and inference operations. |
| 6 | [RAG & Vector Databases](./rag-vector-db/) | Embeddings, chunking, Qdrant, ChromaDB, pgvector, hybrid retrieval, and evaluation. |
| 7 | [AI Agents](./ai-agents/) | Tool use, autonomous workflows, guardrails, and operational agents. |
| 8 | [Model Context Protocol](./mcp/) | MCP architecture, server design, tool/resource exposure, and client integration. |
| 9 | [Orchestration](./orchestration/) | n8n-style workflows, event routing, approvals, and automation pipelines. |
| 10 | [Observability & AIOps](./observability-aiops/) | Metrics, logs, traces, LLM observability, alerting, and incident intelligence. |
| 11 | [AI Security](./ai-security/) | Prompt injection, secrets, data leakage, network policy, and guardrail design. |
| 12 | [Capstone Projects](./projects/) | End-to-end portfolio projects that combine infrastructure, AI, and operations. |

---

## 🛠️ Capstone Projects

| Project | What it teaches | Start here |
| :--- | :--- | :--- |
| Local RAG Assistant | Streamlit, Qdrant, embeddings, Ollama, and local RAG loops. | [`projects/local-rag-assistant/`](./projects/local-rag-assistant/) |
| AI DevOps Copilot | Click CLI, local model prompts, Kubernetes YAML, Terraform generation, and safe fallbacks. | [`projects/ai-devops-copilot/`](./projects/ai-devops-copilot/) |
| AI Log Analysis Pipeline | FastAPI, Vector log routing, LLM-based diagnosis, and simulation mode. | [`projects/ai-log-analysis-pipeline/`](./projects/ai-log-analysis-pipeline/) |
| Kubernetes AI Platform | GPU inference, vLLM/KServe manifests, KEDA scaling, and Terraform GPU infrastructure. | [`projects/kubernetes-ai-platform/`](./projects/kubernetes-ai-platform/) |
| AI SRE Agent | Alertmanager webhooks, Kubernetes diagnostics, remediation decisions, and safe auto-healing. | [`projects/ai-sre-agent/`](./projects/ai-sre-agent/) |

---

## ⚡ Quick Start

### Option 1: Read and choose a path

```bash
cat QUICKSTART.md
cat ROADMAP.md
cat STUDY_MATERIALS.md
```

### Option 2: Run the AI DevOps Copilot

```bash
cd projects/ai-devops-copilot
python -m pip install -r requirements.txt
python copilot.py generate kubernetes --prompt "nginx deployment with 3 replicas"
```

### Option 3: Run project tests

```bash
python -m pytest projects/*/tests -q
```

> Some labs use Docker, Kubernetes, GPUs, Ollama, or model downloads. When those services are unavailable, several examples include local simulation fallbacks so learners can still inspect the workflow.

---

## 🧰 Recommended Local Tooling

Install these tools as you progress through the roadmap:

- Python 3.10+ or 3.11+
- Docker and Docker Compose
- `kubectl`, Kind or Minikube
- Terraform
- Ollama or another local model runtime
- A code editor with Markdown and Mermaid preview support
- Optional: NVIDIA GPU drivers and CUDA toolkit for GPU labs

---

## ✅ Quality Checks

The repository includes tests and validation workflows for learning projects and examples:

```bash
python -m pytest projects/*/tests -q
python -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
python -m black --check $(git ls-files '*.py')
```

The GitHub Actions workflow also validates Markdown links, YAML syntax, Dockerfiles, and security scanning where supported.

---

## 💡 Suggested Improvements for This Repo

These are the highest-value next improvements to make the repository more useful and production-like:

### Documentation and learning experience

- Add screenshots or short GIF demos for each capstone project.
- Add architecture diagrams to each project README using Mermaid and exported PNG/SVG files.
- Add a glossary for AI infrastructure terms such as KV cache, quantization, embeddings, HNSW, MCP, and guardrails.
- Add beginner, intermediate, and advanced issue labels to guide new contributors.
- Add a progress tracker template that learners can copy into their own fork.

### Project reliability

- Add `.env.example` files for every runnable project.
- Add provider-specific API examples for NVIDIA NIM, Hugging Face Inference Providers, OpenAI-compatible APIs, Gemini, Mistral, and Anthropic.
- Add health checks to all Docker Compose services.
- Add Docker Compose profiles for CPU-only and GPU-enabled modes.
- Add smoke-test scripts for each project under a shared `scripts/` directory.
- Add Make targets at the repository root for `test`, `lint`, `format`, `links`, and `docs`.

### AI platform depth

- Add a vLLM OpenAI-compatible inference demo with request/response examples.
- Add a RAG evaluation notebook or script that scores retrieval quality before and after chunking changes.
- Add a model-serving benchmark comparing Ollama, llama.cpp, vLLM, NVIDIA NIM, Hugging Face Inference Providers, and OpenAI-compatible APIs on the same prompt set.
- Add examples for prompt-injection testing and output validation.
- Add an MCP server example that exposes safe read-only Kubernetes diagnostics.

### Security and production readiness

- Add Kubernetes NetworkPolicy examples for vector databases and inference services.
- Add RBAC examples for read-only agents and approval-gated remediation agents.
- Add secret-management examples using environment variables, sealed secrets, or cloud secret managers.
- Add threat models for the RAG assistant, AI SRE agent, and DevOps copilot.
- Add audit logging for any agent action that reads infrastructure state or proposes remediation.

### Community and maintainability

- Replace placeholder community links with real community channels when available.
- Add a `CODEOWNERS` file for project/module ownership.
- Add pull request templates for docs, labs, and code changes.
- Add a release checklist for major curriculum updates.
- Add a public project board or milestone list for the next roadmap improvements.

---

## 🤝 Contributing

Contributions are welcome. Good first contributions include:

- Fixing broken links or typos.
- Improving lab instructions.
- Adding diagrams or screenshots.
- Adding tests for project examples.
- Adding security notes and production hardening guidance.

Before opening a PR, read [`CONTRIBUTING.md`](./CONTRIBUTING.md) and keep changes focused.

---

## 📚 More Study Resources

Use these files together:

- [`QUICKSTART.md`](./QUICKSTART.md) for the fastest hands-on entry point.
- [`ROADMAP.md`](./ROADMAP.md) for the 24-week learning plan.
- [`STUDY_MATERIALS.md`](./STUDY_MATERIALS.md) for curated external resources and portfolio ideas.
- [`HOME_LAB_REQUIREMENTS.md`](./HOME_LAB_REQUIREMENTS.md) for home lab, local LLM, API-first, NVIDIA NIM, and Hugging Face setup guidance.
- [`AI_ECOSYSTEM.md`](./AI_ECOSYSTEM.md) for model-fit tools, US/Chinese AI company watchlists, and model selection guidance.
- [`TROUBLESHOOTING.md`](./TROUBLESHOOTING.md) for common setup and runtime issues.
- [`BADGES.md`](./BADGES.md) for learner achievement ideas.

---

## 📄 License

This project is licensed under the [MIT License](./LICENSE).

---

**Build the platform. Operate the intelligence. Document everything.**
