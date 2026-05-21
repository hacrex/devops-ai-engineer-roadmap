# 📊 AI Observability, Distributed Tracing & AIOps

In traditional software, monitoring requests via response codes (200/500) and CPU metrics is sufficient. In **AI Engineering**, applications are non-deterministic, and latencies can span from seconds to minutes. Ensuring performance requires **AI Observability**—tracking token production rates (Tokens per Second), system latencies, retrieval relevance scores, API call trees, and model costs using tools like **OpenTelemetry**, **Langfuse**, and **OpenLIT**.

---

## 🏗️ Distributed AI Trace Map

```
 ┌─────────────────────────────────────────────────────────────┐
 │  USER HTTP REQUEST (Start Span)                             │
 └──────────────────────────────┬──────────────────────────────┘
                                │ (0ms)
                                ▼
 ┌─────────────────────────────────────────────────────────────┐
 │  SPAN 1: Guardrail Check (LlamaGuard API)                   │
 │  - Input security scan (Latency: 80ms)                       │
 └──────────────────────────────┬──────────────────────────────┘
                                │ (80ms)
                                ▼
 ┌─────────────────────────────────────────────────────────────┐
 │  SPAN 2: Vector Search (Qdrant Database)                    │
 │  - Context Retrieval Query (Latency: 15ms)                  │
 └──────────────────────────────┬──────────────────────────────┘
                                │ (95ms)
                                ▼
 ┌─────────────────────────────────────────────────────────────┐
 │  SPAN 3: Inference Engine (vLLM Serving)                    │
 │  - Token generation stream (Latency: 850ms)                 │
 └─────────────────────────────────────────────────────────────┘
```

---

## 📘 Core AI Observability Concepts

### 1. Key AI Performance Metrics (Golden Signals)
When auditing AI pipelines, focus on three primary metrics:
* **Time to First Token (TTFT)**: The latency from the user submitting a prompt to the model returning the first text token. Critical for user experience in interactive chat tools.
* **Inter-Token Latency (ITL)**: The average time taken to generate subsequent tokens. Measures overall GPU generation speed.
* **Tokens Per Second (T/S)**: Total tokens generated divided by execution time. Standard throughput metric.

### 2. Distributed Tracing vs. Traditional Logging
Traditional logs only capture isolated terminal strings. **Distributed Tracing** (using **OpenTelemetry**) groups all sub-actions associated with a single user request into a visual tree of "Spans". This allows developers to immediately identify which downstream component (e.g. database query, guardrail check, model server) is causing a slow API response.

---

## 🛠️ Hands-on Observability Lab: OpenLIT Instrumentation

In this lab, you will write a Python script demonstrating how to instrument an AI application programmatically using **OpenLIT** (an open-source OpenTelemetry wrapper) to collect, format, and export trace maps and metric data automatically.

### Step 1: Install OpenLIT and dependencies
```bash
pip install openlit openai
```

### Step 2: Write the Instrumented Script (`obs_pipeline.py`)
```python
import os
import openlit

# 1. Initialize OpenLIT telemetry collection
# In production, configure environment variables to pipe data to a collector:
# os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "http://otel-collector:4317"

openlit.init(
    application_name="ai-copilot-engine",
    environment="production",
    disabled=False # Enable telemetry exporting
)

print("🟢 OpenLIT telemetry successfully initialized.")

def simulate_llm_run():
    print("🚀 Running mock LLM inference pipeline...")
    
    # OpenLIT automatically patches and instruments standard SDKs like OpenAI, Ollama, and ChromaDB!
    # Below shows how OpenLIT intercepts calls:
    try:
        from openai import OpenAI
        client = OpenAI(
            base_url="http://localhost:11434/v1", # Local Ollama path
            api_key="none"
        )
        
        # This execution is automatically intercepted, and metrics (latency, token counts, cost) are recorded
        response = client.chat.completions.create(
            model="qwen2.5-coder:7b",
            messages=[{"role": "user", "content": "Explain container namespaces in 1 sentence."}],
            temperature=0.0
        )
        print("Model Response:", response.choices[0].message.content)
        
    except Exception as e:
        print("⚠️ Local Ollama server offline! Simulating collected trace metrics...")
        
        # Manual trace logging mock for telemetry validation
        openlit.trace(
            span_name="mock_vllm_completions",
            inputs={"prompt": "Explain container namespaces in 1 sentence."},
            outputs={"response": "Container namespaces isolate system resources (like network or PID trees) in Linux."},
            metrics={
                "input_tokens": 12,
                "output_tokens": 15,
                "latency_seconds": 0.420
            }
        )
        print("Mock telemetry trace generated successfully.")

if __name__ == "__main__":
    simulate_llm_run()
    print("✨ Telemetry spans successfully captured. Inspect on Grafana / Langfuse.")
```

### Step 3: Run the Script
```bash
python obs_pipeline.py
```

---

## ⚡ Production Prometheus Custom Grafana Rules

To track model queue lengths and API latencies inside Kubernetes, configure your Prometheus scraping tools to query vLLM metrics. Below is an example of standard PromQL equations to construct dashboards:

### 📈 Core PromQL Dashboard Queries

* **Average Time to First Token (TTFT)**:
  ```promql
  sum(rate(vllm:time_to_first_token_seconds_sum[5m])) / sum(rate(vllm:time_to_first_token_seconds_count[5m]))
  ```

* **GPU KV-Cache Memory Utilization**:
  ```promql
  vllm:gpu_cache_usage_factor * 100
  ```

* **Request Queue Backlog Density (Scaling Trigger)**:
  ```promql
  sum(vllm:num_requests_waiting)
  ```

---

## 🔒 Security Considerations: PII Scrubbing
1. **PII and Secret Leakage inside traces**: Trace payloads can accidentally store sensitive user data (e.g. names, passwords, API keys) passed in prompts. Configure OpenLIT or Langfuse processors to dynamically redact strings matching regex patterns (social security numbers, emails, API tokens) before sending traces to database servers.
2. **Telemetry Data Access**: Secure access to your tracing databases (Langfuse/Grafana) using multi-factor authentication (MFA) and single sign-on (SSO) configurations.
3. **Encrypted Telemetry Traffic**: Force TLS encryption on your OpenTelemetry OTLP collectors.

---

## 📈 Scaling & Observability Considerations
* **Telemetry Volume and Storage**: Collecting traces on 100% of API requests inside high-concurrency environments will quickly saturate storage disks. Implement **Head-based or Tail-based Sampling** rules in the OpenTelemetry Collector to trace *only* 5-10% of successful queries while capturing 100% of errors.
* **Performance Overhead**: Keep telemetry gathering lightweight. Ensure metrics and traces are queued in memory and exported asynchronously to avoid blocking user threads.

---

## 🔍 Troubleshooting Guide

### 💥 Issue: Traces are Missing in Grafana / Langfuse Dashboards
* **Root Cause**: The application container lacks correct destination environment variables, or port `4317` (OTLP standard port) is blocked by network policies.
* **Mitigation**:
  1. Print env variables inside your container environment to check `OTEL_EXPORTER_OTLP_ENDPOINT` paths.
  2. Verify that network policies permit outgoing egress TCP requests on port `4317` to the target collector service.
  3. Inspect your OpenTelemetry collector container logs (`kubectl logs deployment/otel-collector -n monitoring`) for connection drops or parsing issues.

---

## 🌟 Best Practices & Open-Source Tools
* **Langfuse**: A powerful open-source dashboard specifically designed to trace, evaluate, and monitor complex LLM steps and prompt changes.
* **OpenLIT**: An open-source, auto-patching OpenTelemetry wrapper that instruments LLM calls instantly.
