# 🔌 Model Context Protocol (MCP) & Infrastructure Integrations

The **Model Context Protocol (MCP)**, developed by Anthropic, is an open-standard protocol designed to bridge Large Language Models (LLMs) with external systems. Historically, connecting a coding assistant (like Claude or Copilot) to a local command line, a database, or a Kubernetes cluster required writing ad-hoc, proprietary API wrappers. MCP establishes a unified, secure, and standardized **JSON-RPC** protocol over stdin/stdout or SSE transport layers to expose **Tools, Prompts, and Resources** to AI clients.

---

## 🏗️ MCP Client-Server Topology

```
┌────────────────────────────────────────────────────────────────────────┐
│ MCP CLIENT (Claude Desktop / Cursor / Custom Agent)                    │
│ - Orchestrates LLM Context   - Displays Markdown  - Manages Approvals  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ bi-directional JSON-RPC
                                    ▼ (stdin/stdout or SSE HTTP)
┌────────────────────────────────────────────────────────────────────────┐
│ MCP SERVER (Custom Python/Go Service)                                  │
│ - Exposes Tools (Schema) - Runs Local Queries   - Reads Files/Logs     │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼ Direct API execution
┌────────────────────────────────────────────────────────────────────────┐
│ TARGET SYSTEMS                                                         │
│ Kubernetes API Cluster ────► Local File System ────► PostgreSQL DB      │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 📘 Model Context Protocol Core Concepts

### 1. JSON-RPC Protocol Transport
MCP communication is bi-directional. A client (e.g., Cursor) starts the server process as a background sub-process, sending requests to the server's `stdin` and parsing results returned from the server's `stdout`.
* **Standard Request (Schema Query)**: The client asks: *"What tools do you have?"*
* **Standard Response**: The server returns JSON schemas for its tools: e.g. `list_pods`, `exec_remediation`.

### 2. Prompts, Resources, and Tools
* **Prompts**: Standardized system context templates exposed by the server.
* **Resources**: Static/Dynamic read-only data files (e.g. database schemas, log reports) exposed to the client.
* **Tools**: Executable functions that can modify system states (e.g., restarting a service).

---

## 🛠️ Hands-on Lab: Custom Python MCP Server

In this lab, you will write a complete, standalone Python MCP Server utilizing the official `@modelcontextprotocol/sdk` to expose Kubernetes cluster inspection and remediation tools.

### Step 1: Install MCP SDK
```bash
pip install mcp click
```

### Step 2: Write the MCP Server (`mcp_server.py`)
```python
import os
import sys
import json
import click
from mcp.server.fastmcp import FastMCP

# 1. Initialize FastMCP Server
mcp = FastMCP("ai-infrastructure-manager")

# Simulate a local cluster database state
DEPLOYMENTS_DB = {
    "vllm-serving": {"replicas": 3, "status": "Running", "warnings": 0},
    "qdrant-db": {"replicas": 1, "status": "Degraded", "warnings": 4}
}

# 2. Expose a resource (read-only system report)
@mcp.resource("reports://cluster_health")
def get_health_report() -> str:
    """Returns a real-time status summary of cluster deployments."""
    return json.dumps(DEPLOYMENTS_DB, indent=2)

# 3. Expose a Tool to inspect active deployments
@mcp.tool()
def get_deployment_status(deployment_name: str) -> str:
    """Queries the status and replica settings of a target deployment.
    
    Args:
        deployment_name: The name of the deployment to inspect (e.g. qdrant-db)
    """
    deploy_info = DEPLOYMENTS_DB.get(deployment_name)
    if not deploy_info:
        return f"Error: Deployment '{deployment_name}' not found."
    return f"Deployment '{deployment_name}' status: {json.dumps(deploy_info)}"

# 4. Expose a Tool to repair degraded deployments
@mcp.tool()
def repair_deployment(deployment_name: str) -> str:
    """Attempts to auto-repair and restart a degraded deployment.
    
    Args:
        deployment_name: The name of the deployment to repair (e.g. qdrant-db)
    """
    deploy_info = DEPLOYMENTS_DB.get(deployment_name)
    if not deploy_info:
        return f"Error: Deployment '{deployment_name}' not found."
    
    # Simulate remediation
    deploy_info["status"] = "Running"
    deploy_info["warnings"] = 0
    return f"🔧 Remediated '{deployment_name}' successfully. Deployment is now active."

if __name__ == "__main__":
    # Start the stdin/stdout JSON-RPC server execution loop
    mcp.run()
```

### Step 3: Register the Server in Claude Desktop
To consume your custom MCP server in Claude Desktop, edit your config file:
* **Windows path**: `%APPDATA%\Claude\claude_desktop_config.json`
* **macOS path**: `~/Library/Application Support/Claude/claude_desktop_config.json`

Add your server configuration:
```json
{
  "mcpServers": {
    "infra-manager": {
      "command": "python",
      "args": [
        "d:/Kashvit/My Apps/devops-ai-engineer-roadmap/mcp/mcp_server.py"
      ]
    }
  }
}
```
Restart Claude Desktop. You will notice a plug icon representing your custom infrastructure tools. Try typing: *"Claude, inspect the status of 'qdrant-db' and run repair if it is degraded."*

---

## 🔒 Security Considerations
1. **Tool Invocations Confirmations**: Never run destructive tools (like `repair_deployment` or writing system configurations) without manual user approval. Build an **Approval Interface** in the client app to prompt: *"Run repair_deployment? [Yes/No]"*.
2. **Access Isolation**: Standardize on minimum cluster access. The MCP server process must run using isolated local system user credentials to prevent arbitrary system hacks.
3. **Log Sanitization**: Ensure data returned in Resources or Tool Outputs is sanitized to block system token leaks or secret disclosures.

---

## 📈 Scaling & Observability Considerations
* **Sidecar Deployment**: Run MCP servers as **sidecar containers** next to your core agentic microservices. This divides context gathering layers from execution engines neatly.
* **Network Tracing**: Track protocol connection latencies and JSON-RPC parse exceptions to maintain performance.

---

## 🔍 Troubleshooting Guide

### 💥 Issue: Server Fails to Connect and Claude Desktop Reports "Broken Pipe"
* **Root Cause**: The MCP server script crashed on startup, or printed debug statements using standard `print()`. In MCP, `stdout` is reserved exclusively for raw JSON-RPC protocol payloads. Standard Python prints corrupt the protocol stream.
* **Mitigation**:
  1. Never write `print()` statements in MCP servers! Use standard Python logging redirecting output to `sys.stderr`.
  2. Verify your python path and environment packages match the target script dependencies.
  3. Execute the script manually via the CLI to check for compilation syntax errors.

---

## 🌟 Best Practices & Open-Source Tools
* **FastMCP**: A high-level python SDK to build MCP servers instantly with automatic schema generation and CLI options.
* **Claude Desktop Developer Tools**: Use the built-in system console to inspect JSON-RPC message logs and diagnose connection drops.
