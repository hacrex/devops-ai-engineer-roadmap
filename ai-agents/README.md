# 🤖 Autonomous AI Agents, Multi-Agent Systems & Infrastructure Co-Pilots

In traditional automation, scripts execute static, pre-defined procedures. In **Agentic Engineering**, an **AI Agent** is an autonomous system that uses an LLM as its core reasoning engine to plan steps, execute system tools, observe environments, and dynamically adjust actions to solve complex goals. For Platform and DevOps teams, AI Agents are the future of self-healing infrastructure, smart code generation, and automated SRE operations.

---

## 🏗️ Agentic Execution Loop (ReAct Framework)

```
                       ┌────────────────────────┐
                       │  Start User Goal       │
                       │  (e.g., Fix Memory)    │
                       └───────────┬────────────┘
                                   │
                                   ▼
                       ┌────────────────────────┐
                       │  Reasoning & Planning  │ ◄────────────────┐
                       │  (LLM Thought State)   │                  │
                       └───────────┬────────────┘                  │
                                   │                               │
                                   ▼                               │
                       ┌────────────────────────┐                  │ Iterates
                       │  Tool Execution        │                  │ and
                       │  (run kubectl / bash)  │                  │ Corrects
                       └───────────┬────────────┘                  │
                                   │                               │
                                   ▼                               │
                       ┌────────────────────────┐                  │
                       │  Environment Feedback  │ ─────────────────┘
                       │  (Observe command logs)│
                       └───────────┬────────────┘
                                   │ Goal Reached?
                                   ▼
                       ┌────────────────────────┐
                       │  Deliver final report   │
                       └────────────────────────┘
```

---

## 📘 Core Agentic Engineering Concepts

### 1. The Planning and Memory Stack
* **Planning (ReAct / Chain of Thought)**: The agent breaks down a high-level goal into logical micro-steps. It reasons before acting: *"I need to inspect the logs first, then run a port check."*
* **Short-Term Memory**: The in-context history of conversational dialogue and execution logs.
* **Long-Term Memory**: Vector Databases where past resolved issues are stored, allowing agents to retrieve historical context when encountering similar bugs.

### 2. Multi-Agent Systems
Complex tasks are best solved by assigning roles to multiple specialized agents co-operating in a structured loop.
* **The Developer Agent**: Writes high-performance code.
* **The Security Auditor Agent**: Statically analyzes the code, flagging vulnerabilities and blocking PRs.
* **The Platform SRE Agent**: Orchestrates staging deployments and validates service health checks.

---

## 🛠️ Hands-on Lab: Autonomous SRE Diagnostic Agent

In this lab, you will build an autonomous SRE agent in Python that receives a system outage goal, uses local diagnostic tools, and decides how to remediate the system state dynamically.

### Step 1: Install click and requests
```bash
pip install click requests
```

### Step 2: Write the Autonomous SRE Agent (`sre_agent.py`)
```python
import sys
import json
import httpx

# 1. System Mock State (Simulating local system parameters)
SYSTEM_DISK_USAGE = 92 # 92% full disk
DOCKER_CONTAINER_STATUS = "Exited (137) - OOM Killed"

# 2. Define standard tools the agent can execute
def check_disk_capacity():
    print("🔧 [TOOL EXECUTION] Running 'df -h' on target node...")
    return f"Disk space utilization is currently at {SYSTEM_DISK_USAGE}% capacity. Warning threshold exceeded."

def run_docker_prune():
    global SYSTEM_DISK_USAGE
    print("🔧 [TOOL EXECUTION] Running 'docker system prune -af'...")
    SYSTEM_DISK_USAGE = 42 # Simulate successful cleanup
    return "Docker cleanup complete. Deleted 42GB of dangling caches and build layers."

def restart_broken_pod():
    print("🔧 [TOOL EXECUTION] Running 'kubectl rollout restart deployment/inference'...")
    return "Rollout successfully triggered. 2 active replicas spinning up."

def execute_tool(name):
    if name == "check_disk_capacity":
        return check_disk_capacity()
    elif name == "run_docker_prune":
        return run_docker_prune()
    elif name == "restart_broken_pod":
        return restart_broken_pod()
    else:
        return "Unknown tool."

# 3. Agent Prompts
SYSTEM_INSTRUCTIONS = """You are an Autonomous SRE System Agent. 
Your goal is to diagnose and repair target node outages.
You have access to these exact tool functions:
- check_disk_capacity
- run_docker_prune
- restart_broken_pod

You run in a loop: Reason (Thought), select a tool (Action), and inspect outputs (Observation).
If you want to invoke a tool, output ONLY this JSON format:
{"thought": "Your reasoning here", "action": "tool_name"}

If the outage is successfully repaired, explain the fix and output ONLY this JSON:
{"status": "resolved", "summary": "Detailed resolution report"}"""

def run_agent_loop():
    print("🤖 Launching Autonomous SRE Remediation Agent...")
    
    # Starting context
    messages = [
        {"role": "system", "content": SYSTEM_INSTRUCTIONS},
        {"role": "user", "content": "Goal: The target GPU node reports a memory crash event and disk pressure warning. Analyze issues and repair."}
    ]
    
    # Simulate up to 3 execution steps to prevent infinite loop
    for step in range(3):
        print(f"\n--- [AGENT LOOP STEP {step + 1}] ---")
        
        payload = {
            "model": "qwen2.5-coder:7b",
            "messages": messages,
            "format": "json",
            "options": {"temperature": 0.0}
        }
        
        try:
            response = httpx.post("http://localhost:11434/api/chat", json=payload, timeout=30.0)
            if response.status_code != 200:
                raise ConnectionError
            data = response.json()
            content = data['message']['content']
            parsed = json.loads(content)
        except Exception:
            # Fallback mock sequence to demonstrate agent reasoning loop if local model is offline
            if step == 0:
                parsed = {"thought": "I need to inspect the disk capacity to see if the disk warning is valid.", "action": "check_disk_capacity"}
            elif step == 1:
                parsed = {"thought": "Disk is at 92%. I must clean up unused layers using docker system prune.", "action": "run_docker_prune"}
            else:
                parsed = {"status": "resolved", "summary": "Cleaned up disk space (reduced storage usage from 92% to 42%) and confirmed node is healthy."}

        # Check for final resolution status
        if parsed.get("status") == "resolved":
            print("\n✨ OUTAGE RESOLVED! Final Agent Report:")
            print(f"📄 {parsed.get('summary')}")
            break

        # Process chosen tool action
        action_name = parsed.get("action")
        thought = parsed.get("thought")
        
        print(f"🤔 Thought: {thought}")
        print(f"👉 Choosing Action: {action_name}")
        
        # Execute tool and generate observation
        observation = execute_tool(action_name)
        print(f"👀 Observation: {observation}")
        
        # Append thought, action, and observation back into the conversation context
        messages.append({"role": "assistant", "content": json.dumps(parsed)})
        messages.append({"role": "user", "content": f"Observation result: {observation}"})

if __name__ == "__main__":
    run_agent_loop()
```

---

## 🔒 Security Considerations: Sandboxing & Safety Guardrails
1. **Executing Unsafe Code**: Autonomous agents must never execute commands directly on primary host hardware! Run all agent tool executions inside highly isolated **Docker Sandboxes** or microVM configurations (like **Firecracker**).
2. **Access token leaks**: Ensure agents are restricted from accessing `/var/run/secrets/kubernetes.io/serviceaccount` directories inside Pod environments to prevent arbitrary token reading.
3. **Execution timeouts**: Constrain agent execution loops using maximum timeouts and run budgets to prevent runaway execution costs.

---

## 📈 Scaling & Observability Considerations
* **Agent Distributed Tracing**: Standard APM traces fail to show why an agent made a specific decision. Use tracing platforms like **Langfuse** or **Arize Phoenix** to visualize prompt trees, tool call latencies, and thought branches.
* **Token Caching**: Enable prompt caching at the gateway level (e.g. Anthropic or vLLM caching mechanisms) to reduce token costs as conversational histories grow during execution loops.

---

## 🔍 Troubleshooting Guide

### 💥 Issue: Agent Enters a "Hallucination Loop" calling non-existent tools
* **Root Cause**: The system prompt parameters are too vague, or the model size is too small (e.g. under 7B parameters) to process structured logic.
* **Mitigation**:
  1. Use larger, instruction-tuned models for agent execution (minimum 7B or 14B parameter models like Qwen2.5-Coder).
  2. Implement strict Python verification layers that intercept tool calls, throwing clean syntax errors back to the model: *"Error: Tool 'reboot_system' does not exist. Available tools are: check_disk_capacity, run_docker_prune."*
  3. Simplify system instructions, providing clear schema templates.

---

## 🌟 Best Practices & Open-Source Tools
* **CrewAI / AutoGen**: Highly optimized python frameworks to design cooperative multi-agent systems and event-driven orchestrations.
* **Langfuse**: An open-source observability engine to monitor, evaluate, and trace LLM applications.
