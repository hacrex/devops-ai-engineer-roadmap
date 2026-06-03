# 🌐 AI Ecosystem Watchlist: Tools, Companies, and Models

Use this guide as a living watchlist for model-selection tools, major AI companies, and model families to track while working through the roadmap. AI rankings change quickly, so treat these tables as a starting point and verify current results with live leaderboards before making technical or purchasing decisions.

---

## 🔧 Model Fit and Model Selection Tools

### llmfit

[llmfit](https://www.llmfit.org/) is a hardware-aware model recommendation tool. It detects your RAM, CPU, GPU VRAM, and local runtime providers, then recommends models that should fit your machine.

Use it when you want to answer:

- Which local model can my laptop or GPU actually run?
- Should I use CPU, GPU, CPU+GPU offload, or a different quantization?
- Which model should I choose for coding, chat, RAG, or experimentation?

Example commands:

```bash
# macOS / Linux with Homebrew
brew install llmfit

# Quick install
curl -fsSL https://llmfit.axjns.dev/install.sh | sh

# Explore recommendations
llmfit
llmfit system
llmfit recommend --json --limit 5
llmfit fit --perfect -n 5
```

Good repo improvement idea: add a `scripts/check-llmfit.sh` helper that runs `llmfit system` and stores a hardware-fit report for learners.

### llm-checker

[`llm-checker`](https://www.npmjs.com/package/llm-checker) is an npm-distributed CLI focused on Ollama model selection. Package security/index pages describe it as a hardware-aware Ollama model selector with a packaged model catalog and recommendations across many model variants.

Use it when you want to answer:

- Which Ollama models should I install for this machine?
- Which installed models are too large or inefficient?
- Which model should I use for a specific local workload?

Example commands:

```bash
# Install globally
npm install -g llm-checker

# Run interactively or inspect package help
llm-checker
llm-checker --help
```

Good repo improvement idea: document both `llmfit` and `llm-checker` in local LLM labs so learners can compare independent fit recommendations before downloading large models.

---

## 🇺🇸 Top US AI Companies to Track

This is a practical AI platform engineering watchlist, not a financial ranking. It prioritizes frontier model labs, AI infrastructure providers, cloud platforms, and companies that shape developer workflows.

| Company | Why it matters for this roadmap | Model/product families to watch |
| :--- | :--- | :--- |
| OpenAI | Frontier models, APIs, tools, agents, structured outputs, and ecosystem influence. | GPT, reasoning models, embeddings, image/audio models, agent tooling. |
| Anthropic | Strong long-context and safety-focused models for coding, analysis, and enterprise workflows. | Claude Opus, Claude Sonnet, Claude Haiku. |
| Google DeepMind / Google AI | Frontier multimodal models, TPU/cloud infrastructure, search grounding, and AI research. | Gemini, Gemma, Veo, Imagen. |
| Meta AI | Open-weight model influence, research, and deployment patterns for self-hosted AI. | Llama, Code Llama-style developer models, image/video research models. |
| xAI | Frontier chat/reasoning models and real-time product integration. | Grok model family. |
| NVIDIA | GPU infrastructure, CUDA, NIM, TensorRT-LLM, inference optimization, and AI platform tooling. | NIM microservices, NeMo, TensorRT-LLM, GPU Operator. |
| Microsoft AI / Azure AI | Enterprise AI platform, Azure OpenAI, developer tooling, GitHub integration, and Copilot ecosystem. | Azure AI Foundry, Copilot, GitHub Copilot, hosted model catalog. |
| Amazon / AWS AI | Cloud AI services, Bedrock, Trainium/Inferentia, managed vector and agent services. | Amazon Bedrock, Nova, SageMaker, Q. |
| Databricks / Mosaic AI | Enterprise data + AI platform, model serving, evaluation, ML governance, and lakehouse workflows. | Mosaic AI, DBRX-style models, MLflow. |
| Perplexity AI | Search-grounded answer engines and real-time retrieval/product UX patterns. | Perplexity answer engine, Sonar-style search models. |

---

## 🇨🇳 Top Chinese AI Companies to Track

This is a practical watchlist for model and platform awareness. It focuses on companies with important Chinese model families, cloud platforms, open models, or AI infrastructure relevance.

| Company | Why it matters for this roadmap | Model/product families to watch |
| :--- | :--- | :--- |
| DeepSeek | Highly competitive reasoning/coding models and open-weight releases that influence local LLM workflows. | DeepSeek V/R model families. |
| Alibaba Cloud / Qwen | Strong open and hosted model ecosystem with broad multilingual and coding coverage. | Qwen, Qwen-Coder, Qwen-VL. |
| Baidu | Major Chinese AI platform and search/cloud player with long-running foundation model work. | ERNIE, Wenxin/YiYan ecosystem. |
| Tencent | Large AI/cloud ecosystem with foundation models and enterprise integration. | Hunyuan model family. |
| ByteDance | Large consumer AI distribution, recommendation infrastructure, and model development. | Doubao, Seed model families. |
| Moonshot AI | Long-context and assistant-oriented model development. | Kimi, Kimi K-series. |
| Zhipu AI | GLM model family and developer-facing model/API ecosystem. | GLM, CodeGeeX. |
| MiniMax | Multimodal and assistant model ecosystem with consumer and developer products. | MiniMax, abab-style model families. |
| SenseTime | Computer vision heritage, enterprise AI, and large model platforms. | SenseNova / SenseChat ecosystem. |
| Huawei | AI chips, cloud infrastructure, and model/platform stack relevance in China. | Pangu models, Ascend ecosystem. |

---

## 🏆 Top Model Families to Watch

There is no single permanent top model. Use this table to choose what to evaluate for your workload, then verify with live benchmarks such as [LMArena](https://arena.ai/leaderboard/), [Artificial Analysis](https://artificialanalysis.ai/), provider docs, and your own task-specific evals.

| Category | Model families to watch | Why they matter |
| :--- | :--- | :--- |
| General frontier reasoning | GPT, Claude Opus/Sonnet, Gemini Pro/Ultra, Grok | Strong general-purpose reasoning, coding, tool use, and multimodal capabilities. |
| Open / open-weight local models | Llama, Qwen, DeepSeek, Mistral, Gemma, GLM | Important for local labs, self-hosting, privacy, and cost control. |
| Coding | GPT, Claude Sonnet, Gemini, DeepSeek Coder, Qwen Coder, Codestral-style models | Use for DevOps copilot, CI/CD generation, Terraform, Kubernetes YAML, and code review. |
| RAG and enterprise search | GPT, Claude, Gemini, Qwen, Cohere-style retrieval models, embedding/reranker models | Use for retrieval quality, citations, reranking, and structured answers. |
| Multimodal | Gemini, GPT multimodal, Claude multimodal, Qwen-VL, Llama vision variants | Use for diagrams, screenshots, incident images, document understanding, and video/image labs. |
| Low-latency / edge | Small Llama, Phi, Gemma, Qwen small models, MiniCPM-style models | Useful for laptops, edge devices, CPU-only demos, and fast local iteration. |
| China frontier models | DeepSeek, Qwen, Kimi, GLM, ERNIE, Hunyuan, Doubao | Important for comparing global model ecosystems, multilingual performance, and open model availability. |

### Model selection checklist

Before picking a model for a lab or project, evaluate:

- **Task fit:** coding, RAG, agent tools, summarization, multimodal, or low-latency chat.
- **Deployment mode:** local CPU, local GPU, hosted API, NIM, Hugging Face, or Kubernetes inference.
- **Context length:** enough tokens for logs, docs, or runbooks.
- **Cost:** API price, GPU rental cost, and operational overhead.
- **Latency:** first-token latency and tokens/second.
- **License:** whether the model can be used for your intended personal, commercial, or enterprise scenario.
- **Safety:** prompt injection resistance, output validation, data handling, and audit requirements.

---

## 📌 Repo Improvements to Add Next

- Add `scripts/check-llmfit.sh` to generate a hardware-to-model fit report.
- Add `scripts/check-llm-checker.sh` for Ollama-focused model recommendations.
- Add `docs/model-selection-matrix.md` comparing local, API, NIM, Hugging Face, and Kubernetes deployment paths.
- Add `.env.example` provider blocks for OpenAI, Anthropic, Gemini, Mistral, NVIDIA, Hugging Face, and local Ollama.
- Add model benchmark templates that record model name, provider, latency, cost, context length, and qualitative task score.
- Add a monthly “model watchlist update” issue template so contributors can refresh model/company tables without rewriting the roadmap.
