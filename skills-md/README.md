# 📜 Agentic Control Files: Skills.md & Prompt Orchestration Specs

When working with autonomous AI engineering agents (such as Claude, Copilot, or Devin), managing their behavior through standard conversational prompts is prone to instruction drift. **`skills.md`** is a declarative configuration system designed to define precise capabilities, behavioral parameters, execution rules, and security limits for operational agents.

---

## 🏗️ Agent Behavior Control Engine

```
 ┌──────────┐  Exposes Limits   ┌──────────┐  Parses and Valid  ┌──────────┐
 │ DevOps   │ ────────────────► │ Skills   │ ─────────────────► │ AI Agent │
 │ Platform │                   │ Spec     │                    │ Runtime  │
 └──────────┘                   └──────────┘                    └────┬─────┘
                                                                     │
                                                                     ▼ Executes under bounds
 ┌──────────┐  Block Violations ┌──────────┐  Forks execution   ┌──────────┐
 │ Safe     │ ◄──────────────── │ Sandbox  │ ◄───────────────── │ Command  │
 │ OS state │                   │ Watcher  │                    │ Executor │
 └──────────┘                   └──────────┘                    └──────────┘
```

---

## 📘 Essential Skills.md Design Concepts

### 1. Capabilities vs. Restrictions
A production-grade agentic control spec divides agent roles explicitly:
* **Capabilities**: The specific terminal tools, API endpoints, or database tables the agent has permission to interact with.
* **Restrictions**: Security boundaries. Explicit rules detailing what actions are strictly forbidden (e.g. modifying core VPC configurations, making destructive database queries, deleting branches).

### 2. Error Recovery & Fallbacks
If a tool execution fails (e.g., a Terraform plan throws an error), the control file instructs the agent exactly how to recover:
* Avoid repeating the exact failing query more than 3 times (anti-loop rule).
* Gather host system diagnostic data and prompt the user for input.

---

## 🛠️ Production-Grade `skills.md` Spec Template

Below is a copy-pasteable, production-ready `skills.md` manifest designed to control an **AI SRE Remediation Agent** operating inside a production Kubernetes cluster.

```markdown
# 🩺 AI Agent Skill & Behavioral Configuration (SRE Role)

This document establishes the boundaries, capabilities, and procedural rules for the SRE remediation agent.

## 1. Persona and Scope
- **Role**: Junior Site Reliability Engineer.
- **Mission**: Automate the identification, diagnostics, and safe recovery of cluster pod failures.
- **Constraint**: You operate in read-write-once mode. All destructive operations (rebooting, rolling back, patching) require explicit manual user approval.

## 2. Capabilities
You are authorized to execute the following tools:
- `kubectl get pods`, `kubectl describe pod`, `kubectl logs --tail=100`.
- Standard read-only API requests targeting the internal Prometheus monitoring server.
- Logging execution histories to standard system trace outputs.

## 3. Strict Prohibitions
Under no circumstances are you allowed to:
- Delete namespaces completely (`kubectl delete namespace`).
- Modify cluster RBAC roles, ServiceAccounts, or Secrets.
- Execute raw bash shell scripts on primary master nodes.
- Make external outbound API calls to unapproved third-party registries.

## 4. Error Resolution Playbook
If an command fails to execute:
1. **Log the error**: Extract the exact stderr return code.
2. **Analysis**: Do not retry the exact same command. Attempt to find alternative diagnostic scripts (e.g., if `kubectl logs` fails due to terminating state, try `kubectl describe`).
3. **Loop Defense**: If the same error repeats 3 times consecutively, stop execution, compile a detailed summary, and ask the USER for instructions.

## 5. Security Boundary
- **Sanitization**: Before outputting logs in comments, redact all API keys, base64 tokens, passwords, and private company domains.
- **Audit Logging**: Every action you execute must start with an audit note explaining the exact rationale behind the chosen tool.
```

---

## 🔒 Security Considerations
1. **Version Control**: Store `skills.md` inside a protected root folder (e.g. `.github/skills.md` or `.cursorrules`) with strict git branch protection. This prevents developers from accidentally diluting agent safety parameters during standard coding cycles.
2. **Sandbox Enforcement**: Ensure the agent execution engine validates command queues against `skills.md` rules programmatically before starting subprocess loops.
3. **Audit Trails**: Run a system logger next to the agent that captures all thought states, tool selections, and user approvals to guarantee complete compliance.

---

## 📈 Scaling & Observability Considerations
* **Context Preservation**: Keep your `skills.md` file compact and highly structured. Massively verbose rules (e.g. 50 pages of instructions) will congest the agent's context window, increasing system latencies and token usage.
* **Token Splicing**: Programmatically inject `skills.md` instructions dynamically only when specific tasks (e.g., code audits, cluster fixes) are instantiated, keeping routine chats fast and efficient.

---

## 🔍 Troubleshooting Guide

### 💥 Issue: Agent Ignores `skills.md` Restrictions (Instruction Drift)
* **Root Cause**: The core model is too small, or the user's conversational prompt contains instructions that counteract the control configurations (a form of prompt override).
* **Mitigation**:
  1. Leverage highly capable models (like Claude 3.5 Sonnet or GPT-4o) that are optimized for instruction adherence.
  2. Implement an API Gateway interceptor (e.g. a Python script) that parses the agent's chosen tools and halts execution if the command violates `skills.md` rules, regardless of what the LLM generated.

---

## 🌟 Best Practices & Open-Source Tools
* **.cursorrules**: A widely adopted local rule structure to govern Cursor coding agents.
* **System Guardrails**: Always enforce double-check scripts at the system API level rather than relying completely on model instruction compliance.
