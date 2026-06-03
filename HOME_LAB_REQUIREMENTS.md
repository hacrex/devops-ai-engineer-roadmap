# 🧰 Home Lab & Local LLM Requirements

This guide helps you choose hardware or cloud APIs for the labs in this repository. You do **not** need an expensive GPU to start: the recommended path is to begin API-first, then add local CPU/GPU inference when you are ready to learn model operations.

> **Rule of thumb:** use cloud APIs for learning application patterns quickly, use local LLMs to learn privacy/offline workflows, and use GPU labs when you want to practice production AI platform operations.

---

## ✅ Minimum Requirements by Learning Mode

| Mode | Best for | Minimum hardware | Recommended hardware |
| :--- | :--- | :--- | :--- |
| API-first laptop | Prompting, agents, RAG app logic, CI/CD, docs, Python labs | 4 CPU cores, 8 GB RAM, 30 GB free disk, stable internet | 4-8 CPU cores, 16 GB RAM, 100 GB SSD |
| CPU-only local LLM | Learning Ollama/llama.cpp concepts with small quantized models | 4-6 CPU cores, 16 GB RAM, 50-100 GB SSD | 8+ CPU cores, 32 GB RAM, NVMe SSD |
| Starter NVIDIA GPU | 7B-class quantized models, embeddings, small RAG demos | NVIDIA GPU with 8 GB VRAM, 32 GB system RAM | 12-16 GB VRAM, 32-64 GB RAM, NVMe SSD |
| Recommended local AI workstation | Faster local LLMs, RAG, vLLM experiments, Docker Compose stacks | 12 GB VRAM, 64 GB RAM, 1 TB NVMe | 16-24 GB VRAM, 64-128 GB RAM, 1-2 TB NVMe |
| Advanced AI platform lab | Kubernetes GPU scheduling, vLLM/KServe, observability, multi-service demos | 24 GB VRAM or cloud GPU, 64 GB RAM | 24-48+ GB VRAM, 128 GB RAM, 2 TB NVMe |
| Kubernetes home lab | Multi-node scheduling, networking, storage, monitoring | One node: 4 CPU cores, 16 GB RAM, 100 GB SSD | 3 nodes: 4-8 CPU cores each, 16-32 GB RAM each, SSD storage |

---

## 🏠 Suggested Home Lab Builds

### 1. Budget learning setup

Use this if you are just starting and want to avoid buying GPU hardware.

- Laptop or mini PC with 16 GB RAM.
- Docker Desktop or Docker Engine.
- Python 3.10+ or 3.11+.
- Ollama for small local models, plus cloud APIs for larger tasks.
- Best labs: prompt engineering, Python automation, RAG app flow, API-based agents, CI/CD, docs.

### 2. Practical local LLM workstation

Use this if you want to run useful small/medium local models.

- 8+ CPU cores.
- 32-64 GB RAM.
- NVIDIA GPU with 12-16 GB VRAM, or Apple Silicon with 32 GB unified memory.
- 1 TB NVMe SSD for model files, containers, vector DB data, and logs.
- Best labs: Ollama, local RAG, embeddings, log analysis, local copilot, small model benchmarking.

### 3. Advanced GPU platform lab

Use this if your goal is Kubernetes AI infrastructure.

- NVIDIA GPU with 24 GB+ VRAM, or a cloud GPU instance.
- 64-128 GB RAM.
- 1-2 TB NVMe SSD.
- Ubuntu Linux recommended for fewer driver/runtime issues.
- NVIDIA driver, NVIDIA Container Toolkit, Docker, Kubernetes, and Helm.
- Best labs: NVIDIA GPU Operator, vLLM, KServe, KEDA, GPU metrics, AI platform observability.

---

## 🧠 Local LLM Sizing Guide

| Model type | Typical local target | Suggested memory profile | Notes |
| :--- | :--- | :--- | :--- |
| Embedding models | `all-MiniLM`, `bge-small`, similar | 8-16 GB RAM is usually enough | Great for RAG labs before running a local chat model. |
| 1B-3B LLMs | Small assistants and fast demos | 8-16 GB RAM or small GPU | Best for low-end laptops and quick tests. |
| 7B-8B quantized LLMs | Practical local chat/coding demos | 16-32 GB RAM, 8-12 GB VRAM preferred | Good default for local Ollama labs. |
| 13B-14B quantized LLMs | Better reasoning/coding at lower speed | 32-64 GB RAM, 16 GB VRAM preferred | Useful when quality matters more than speed. |
| 30B+ models | Advanced experimentation | 24 GB+ VRAM or cloud GPU | Prefer cloud APIs or rented GPU unless you already own the hardware. |

Ollama documents NVIDIA GPU support around CUDA-capable GPUs and notes supported NVIDIA driver expectations in its hardware support page. Always confirm your GPU and driver against the current [Ollama hardware support documentation](https://docs.ollama.com/gpu).

---

## ☁️ Cloud-Based API Options

Use cloud APIs when your laptop cannot run the model you need, when you want fast experimentation, or when the learning objective is application design rather than GPU operations.

| Provider | Good for | Start here | Environment variable |
| :--- | :--- | :--- | :--- |
| OpenAI API | General LLM apps, structured outputs, tools, agents, evals | [OpenAI API Reference](https://platform.openai.com/docs/api-reference) | `OPENAI_API_KEY` |
| Anthropic Claude API | Long-context reasoning, analysis, writing, agent workflows | [Claude API Docs](https://platform.claude.com/docs/claude/reference/overview) | `ANTHROPIC_API_KEY` |
| Google Gemini API | Multimodal prompts, Google ecosystem experiments | [Gemini API Reference](https://ai.google.dev/api) | `GEMINI_API_KEY` |
| Mistral API | Open-weight-aligned model workflows and European provider option | [Mistral API Docs](https://docs.mistral.ai/api) | `MISTRAL_API_KEY` |
| NVIDIA NIM API Catalog | Hosted optimized NIM endpoints, GPU-accelerated prototyping | [NVIDIA API Catalog Quickstart](https://docs.api.nvidia.com/nim/docs/api-quickstart) | `NVIDIA_API_KEY` |
| Hugging Face Inference Providers | Access to many providers through one token and OpenAI-compatible chat routing | [Hugging Face Inference Providers](https://huggingface.co/docs/inference-providers/index) | `HF_TOKEN` |

### API safety checklist

- Never commit API keys to Git.
- Use `.env` files locally and add `.env.example` files for documentation.
- Set monthly budgets, spend alerts, and rate limits where the provider supports them.
- Log model name, latency, token usage, and error rate for every API-backed app.
- Keep a local simulation fallback for demos and tests so CI does not depend on paid services.

---

## 🟢 NVIDIA NIM Free Build Resources and API Path

NVIDIA NIM is useful when you want to learn optimized inference without building the full serving stack yourself.

### What to use

- [build.nvidia.com](https://build.nvidia.com/) to browse NIM microservices and hosted API endpoints.
- [NVIDIA API Catalog Quickstart](https://docs.api.nvidia.com/nim/docs/api-quickstart) to create an API key and call a hosted NIM endpoint.
- [Run NIM Anywhere](https://docs.api.nvidia.com/nim/docs/run-anywhere) for hosted endpoints, local deployment, cloud deployment, and pricing/licensing guidance.
- [NVIDIA NIM for LLMs documentation](https://docs.nvidia.com/nim/large-language-models/latest/introduction.html) for self-hosting LLM NIM containers.
- [NVIDIA Brev](https://www.brev.dev/) if you want a preconfigured cloud GPU development environment.

### Free/prototyping note

NVIDIA's NIM documentation states that NVIDIA Developer Program members have free access to NIM API endpoints for prototyping and to downloadable NIM microservices for research, application development, and experimentation on supported infrastructure. Terms, model availability, and rate limits can change, so check the current NVIDIA pages before planning a workshop or production demo.

### Basic NIM API workflow

```bash
# 1. Create an API key from a model page on build.nvidia.com
export NVIDIA_API_KEY="your_api_key_here"

# 2. Install an OpenAI-compatible client
python -m pip install openai

# 3. Point your client at the NVIDIA-hosted endpoint shown in the model page sample code
#    and keep the model name aligned with the selected NIM catalog model.
```

Use NIM in this roadmap for:

- API-first labs when you do not own a GPU.
- Comparing hosted inference with local Ollama/vLLM behavior.
- Learning how optimized model microservices are packaged and deployed.
- Moving from hosted API prototypes to self-hosted GPU inference.

---

## 🤗 Hugging Face Requirements and API Path

Hugging Face is useful for model discovery, datasets, embeddings, Spaces, and serverless/provider-backed inference.

### What to use

- [Hugging Face Hub](https://huggingface.co/models) for model discovery.
- [Hugging Face Learn](https://huggingface.co/learn) for structured learning.
- [Inference Providers](https://huggingface.co/docs/inference-providers/index) for serverless inference through Hugging Face and partner providers.
- [huggingface_hub InferenceClient](https://huggingface.co/docs/huggingface_hub/en/package_reference/inference_client) for Python applications.
- [Hugging Face Spaces](https://huggingface.co/docs/hub/spaces) for sharing demos.

### Basic Hugging Face API workflow

```bash
python -m pip install huggingface_hub
export HF_TOKEN="your_hugging_face_token_here"
```

```python
import os
from huggingface_hub import InferenceClient

client = InferenceClient(api_key=os.environ["HF_TOKEN"])
response = client.chat_completion(
    model="deepseek-ai/DeepSeek-R1",
    messages=[{"role": "user", "content": "Explain Kubernetes GPU scheduling simply."}],
)
print(response.choices[0].message.content)
```

Use Hugging Face in this roadmap for:

- Finding embedding models for RAG labs.
- Comparing model licenses and model cards.
- Testing hosted inference before downloading a model locally.
- Publishing demos as Spaces.
- Building datasets for evaluation and fine-tuning experiments.

---

## 🧪 Which Path Should I Choose?

| Your situation | Recommended path |
| :--- | :--- |
| I only have a normal laptop. | Start API-first, run small Python/RAG labs locally, and use NIM/Hugging Face/OpenAI-compatible APIs for model calls. |
| I have 16 GB RAM but no GPU. | Run small local models slowly, use APIs for larger models, and focus on application architecture. |
| I have an 8-12 GB NVIDIA GPU. | Run 7B/8B quantized local models, embeddings, local RAG, and simple Docker Compose labs. |
| I have a 24 GB NVIDIA GPU. | Add vLLM, larger quantized models, GPU monitoring, and single-node Kubernetes GPU experiments. |
| I want production platform skills. | Use cloud GPU instances or NIM/Brev for GPU labs, then reproduce the deployment patterns locally or in Kubernetes. |

---

## 📌 Repo Improvements to Add Next

To make hardware/API onboarding even smoother, add these future repo improvements. See [`AI_ECOSYSTEM.md`](./AI_ECOSYSTEM.md) for model-fit tools, company watchlists, and top model families to evaluate:

- `.env.example` files for OpenAI, NVIDIA, Hugging Face, Gemini, Mistral, and Anthropic API keys.
- A `scripts/check-hardware.sh` script that reports CPU, RAM, disk, GPU, CUDA, Docker, and Kubernetes readiness.
- A `scripts/check-api-keys.py` script that verifies configured provider keys without printing secrets.
- Docker Compose profiles for `cpu`, `gpu`, and `api-only` modes.
- A local benchmark script that records tokens/second, latency, memory use, and model name.
- Cost tracking examples for API-backed labs.
- A provider abstraction layer so projects can switch between Ollama, OpenAI-compatible APIs, NVIDIA NIM, and Hugging Face.
