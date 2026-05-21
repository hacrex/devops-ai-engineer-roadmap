# 🎛️ AI Workflow Automation & Agentic Orchestration: n8n & Sim.io

Running terminal scripts manually limits automation scaling. **Orchestration Engines** like **n8n** and **sim.io** enable DevOps teams to design event-driven, visual, and programmatic AI automation pipelines. These pipelines trigger AI agents, parse webhooks, connect databases, handle loop logic, and interface with third-party software (Slack, GitHub, Jira) using robust node-based architectures.

---

## 🏗️ Event-Driven SRE Auto-Remediation Pipeline

```
 ┌───────────────┐  HTTP POST Webhook  ┌───────────────────┐
 │ Prometheus    │ ──────────────────► │  n8n Webhook Node │
 │ Alertmanager  │                     └─────────┬─────────┘
 └───────────────┘                               │
                                                 ▼
 ┌───────────────┐  Analyze & Diagnose   ┌───────────────────┐
 │  Local LLM    │ ◄───────────────────► │  n8n Parser Node  │
 │  (vLLM API)   │                       └─────────┬─────────┘
 └───────────────┘                               │
                                                 ▼
 ┌───────────────┐    Send Alert Report  ┌───────────────────┐
 │ Slack Portal  │ ◄──────────────────── │  Slack HTTP Node  │
 └───────────────┘                       └───────────────────┘
```

---

## 📘 Automation Orchestration Core Concepts

### 1. Webhook Triggers
Webhooks act as event listeners. When a system state changes (e.g. a Git Pull Request is opened, a Prometheus alert fires, or a Slack message is sent), the system makes an HTTP POST request to the orchestration engine containing the event payload.

### 2. Node-Based Chaining & Prompt Routing
Orchestrators allow engineers to route data through logical sequences:
* **The Parser Node**: Extracts relevant text parameters (e.g. Pod Name, Error Code) from the payload.
* **The LLM Node**: Passes the extracted fields inside a prompt template to the model.
* **The Conditional Router**: If the model output indicates an emergency, route the task to a system API; if standard, log to files.

---

## 🛠️ Hands-on Lab: n8n Auto-Healing SRE Webhook Flow

In this lab, you will configure a complete, deployable n8n workflow JSON that listens for a system crash alert, prompts a local LLM to draft a resolution manual, and outputs a diagnostic Slack notification.

### Step 1: Deploy n8n in Docker
```bash
docker run -d --name n8n-server -p 5678:5678 -v n8n_data:/home/node/.n8n n8nio/n8n:latest
```
Access the n8n console at `http://localhost:5678`.

### Step 2: Import the SRE Auto-Healing Workflow JSON
In the n8n dashboard, click **Import from File** or copy-paste this JSON configuration representational schema:

```json
{
  "name": "Prometheus Alert AI Diagnostician",
  "nodes": [
    {
      "parameters": {
        "path": "prometheus-alert",
        "options": {}
      },
      "id": "webhook-trigger-node",
      "name": "Webhook Trigger",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [100, 300]
    },
    {
      "parameters": {
        "jsCode": "const alertData = $input.first().json.body;\nreturn {\n  podName: alertData.alerts[0].labels.pod,\n  errorDescription: alertData.alerts[0].annotations.description,\n  severity: alertData.alerts[0].labels.severity\n};"
      },
      "id": "js-parser-node",
      "name": "Extract Alert Fields",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [300, 300]
    },
    {
      "parameters": {
        "model": "qwen2.5-coder:7b",
        "prompt": "=Analyze this Kubernetes alert for Pod: {{ $json.podName }}.\nError Description: {{ $json.errorDescription }}\nSeverity: {{ $json.severity }}\n\nProvide a concise 3-bullet diagnosis and recommend the exact troubleshooting commands.",
        "options": {}
      },
      "id": "local-llm-node",
      "name": "Inquire Local LLM",
      "type": "n8n-nodes-base.openAi",
      "typeVersion": 1,
      "position": [500, 300]
    },
    {
      "parameters": {
        "chatId": "sre-alerts-channel",
        "text": "=🩺 *AI Diagnostic Report: Cluster Outage*\n\n*Target Pod:* {{ $node[\"Extract Alert Fields\"].json.podName }}\n*Severity:* {{ $node[\"Extract Alert Fields\"].json.severity }}\n\n*AI Recommendation:*\n{{ $json.choices[0].message.content }}"
      },
      "id": "slack-sender-node",
      "name": "Send Slack Alert",
      "type": "n8n-nodes-base.slack",
      "typeVersion": 2,
      "position": [700, 300]
    }
  ],
  "connections": {
    "Webhook Trigger": {
      "main": [
        [{"node": "Extract Alert Fields", "type": "main", "index": 0}]
      ]
    },
    "Extract Alert Fields": {
      "main": [
        [{"node": "Inquire Local LLM", "type": "main", "index": 0}]
      ]
    },
    "Inquire Local LLM": {
      "main": [
        [{"node": "Send Slack Alert", "type": "main", "index": 0}]
      ]
    }
  }
}
```

### Step 3: Test Webhook Pipeline using curl
Locate your n8n webhook URL from the interface, and simulate an Alertmanager alert:
```bash
curl -X POST http://localhost:5678/webhook-test/prometheus-alert \
  -H "Content-Type: application/json" \
  -d '{
    "alerts": [
      {
        "labels": {
          "pod": "vllm-inference-67fc-xx",
          "severity": "critical"
        },
        "annotations": {
          "description": "Container terminated. Exit Code 137 (OOMKilled) on GPU allocation index 0."
        }
      }
    ]
  }'
```
You will immediately see the workflow trigger in n8n, parse the alert body, query your local LLM, and output the diagnostic report!

---

## 🔒 Security Considerations
1. **Webhook Authentication**: Never expose public, unauthenticated webhook URLs! Protect your n8n endpoints using Basic Auth, SSL/TLS certifications, or custom header authorization keys.
2. **Access Token Encapsulation**: Keep database, Slack, and cloud credentials inside n8n's centralized, encrypted **Credential Store** rather than typing them inside javascript or code nodes.
3. **Data Sanitization**: Sanitize incoming parameters before passing them directly into Python runtimes or database queries to prevent SQL or command injection hacks.

---

## 📈 Scaling & Observability Considerations
* **Distributed Executions**: As event volumes grow to thousands of webhooks hourly, scale n8n horizontally on Kubernetes using Redis as an execution queue backend.
* **Alerting on failure**: Set up centralized Error Workflows within n8n that automatically alert on node failures or timeout errors during LLM queries.

---

## 🔍 Troubleshooting Guide

### 💥 Issue: LLM Node Queries Timeout or Hanging
* **Root Cause**: The model serving engine (e.g. Ollama or vLLM) is saturated, or the network routing path between n8n and the model server is congested.
* **Mitigation**:
  1. Increase the connection timeout limits inside the n8n HTTP node (standardize on a 60-second limit).
  2. Implement concurrency limits inside the vLLM engine settings.
  3. Ensure n8n and the model server reside within the same local VPC network or Kubernetes cluster.

---

## 🌟 Best Practices & Open-Source Tools
* **n8n**: The premier, open-source workflow automation platform with dedicated support for advanced AI and LangChain components.
* **Sim.io**: A lightweight, cloud-native event-driven automation framework designed for fast microservices orchestration.
