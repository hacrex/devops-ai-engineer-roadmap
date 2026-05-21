# 🐍 Python for Infrastructure Automation & Kubernetes Operations

In modern Platform and AI Engineering, shell scripts are insufficient for managing complex workflows. Python is the dominant scripting tool for orchestrating model deployments, automating Kubernetes configurations, monitoring GPU clusters, and executing event-driven remediation. A DevOps AI Engineer must master async network communications, building custom CLI utilities, and programmatically interfacing with the Kubernetes API using `kubernetes-client`.

---

## 🏗️ Python Automation Workflow Engine

```
                             ┌───────────────────────┐
                             │  Trigger Event        │
                             │  (Webhook, Cron, CLI) │
                             └───────────┬───────────┘
                                         │
                                         ▼
                             ┌───────────────────────┐
                             │  Python Auth Engine   │
                             │  (Kubeconfig / IAM)   │
                             └───────────┬───────────┘
                                         │
                      ┌──────────────────┴──────────────────┐
                      ▼                                     ▼
          ┌───────────────────────┐             ┌───────────────────────┐
          │  Kubernetes API call  │             │  External REST Call   │
          │  (Read pods, events)  │             │  (Model query, logs)  │
          └───────────┬───────────┘             └───────────┬───────────┘
                      │                                     │
                      └──────────────────┬──────────────────┘
                                         ▼
                             ┌───────────────────────┐
                             │ Parse, Audit, Remed   │
                             │ (Restart Pod, Alert)  │
                             └───────────────────────┘
```

---

## 📘 Core Automation Paradigms

### 1. The Kubernetes Python Client
Instead of writing complex, shell-nested bash scripts that wrap `kubectl`, Python leverages the official `kubernetes` client library. This provides static types, exception handling, and deep configuration parsing to interact with cluster API resources programmatically.

### 2. Async I/O for High-Concurrency Scripting
When fetching logs from 100+ failing container pods, running standard synchronous loops (`requests`) blocks the execution thread, causing the process to hang. Using **`httpx`** and **`asyncio`** enables concurrent API calls, accelerating network checks by up to 10x.

---

## 🛠️ Hands-on Lab: Kubernetes Cluster Diagnostician CLI

In this lab, you will write a complete, standalone Python CLI utility. This tool queries a targeted Kubernetes namespace, filters out GPU-enabled Pods, detects any that are in a `Warning` or `Failed` state, and automatically extracts their logs and event lists for immediate diagnosis.

### Step 1: Install Dependencies
```bash
pip install kubernetes click tabulate
```

### Step 2: Write the Diagnostic CLI Script (`diagnose.py`)
```python
import os
import click
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from tabulate import tabulate

def initialize_kube_client():
    """Initializes and returns the Kubernetes CoreV1Api client."""
    try:
        # Try local in-cluster config first (if running inside a K8s Pod)
        config.load_incluster_config()
    except config.ConfigException:
        try:
            # Fallback to local Kubeconfig file
            config.load_kube_config()
        except config.ConfigException:
            click.secho("Error: Could not locate active Kubeconfig or cluster credentials.", fg="red", bold=True)
            raise SystemExit(1)
    
    return client.CoreV1Api()

@click.command()
@click.option('--namespace', '-n', default='default', help='Target Kubernetes namespace to audit')
@click.option('--lines', '-l', default=15, help='Number of log lines to extract from failing pods')
def main(namespace, lines):
    """🩺 DevOps AI Cluster Diagnostician Tool

    Queries cluster pods, identifies GPU allocations, and extracts crash events and logs.
    """
    click.secho(f"🚀 Initializing audit on namespace: {namespace}...", fg="cyan", bold=True)
    v1 = initialize_kube_client()

    try:
        # 1. List all Pods in the specified namespace
        pods = v1.list_namespaced_pod(namespace)
    except ApiException as e:
        click.secho(f"API Error connecting to Kubernetes: {e}", fg="red")
        return

    pod_table = []
    failing_pods = []

    for pod in pods.items:
        name = pod.metadata.name
        status = pod.status.phase
        
        # Check if the pod requests a GPU
        has_gpu = False
        for container in pod.spec.containers:
            limits = container.resources.limits or {}
            if 'nvidia.com/gpu' in limits:
                has_gpu = True
                break

        gpu_status = "🟢 Yes" if has_gpu else "⚪ No"
        pod_table.append([name, status, gpu_status])

        # Track pods that are not in Running or Succeeded status
        if status not in ["Running", "Succeeded"]:
            failing_pods.append(pod)

    # 2. Print pod status table
    click.echo("\n### Cluster Pods Status Overview")
    click.echo(tabulate(pod_table, headers=["Pod Name", "Status", "GPU Configured"], tablefmt="fancy_grid"))

    if not failing_pods:
        click.secho("\n✨ All pods in this namespace are healthy!", fg="green", bold=True)
        return

    # 3. Diagnose failing pods
    click.secho(f"\n⚠️ Found {len(failing_pods)} failing pods! Commencing diagnostics...", fg="yellow", bold=True)
    
    for pod in failing_pods:
        pod_name = pod.metadata.name
        click.secho(f"\n--- Diagnosing Pod: {pod_name} ---", fg="yellow", underline=True)
        
        # Get Pod Events
        try:
            events = v1.list_namespaced_event(namespace, field_selector=f"involvedObject.name={pod_name}")
            click.echo("Recent Pod Events:")
            for event in events.items[-3:]: # Show last 3 events
                click.echo(f"  [{event.type}] {event.reason} - {event.message}")
        except Exception as e:
            click.echo(f"  Could not pull events: {e}")

        # Get Pod Container Logs
        for container in pod.spec.containers:
            container_name = container.name
            click.echo(f"\nTail of logs for container '{container_name}':")
            try:
                # Read logs from the container
                logs = v1.read_namespaced_pod_log(
                    name=pod_name,
                    namespace=namespace,
                    container=container_name,
                    tail_lines=lines
                )
                click.secho(logs, fg="white", dim=True)
            except ApiException as e:
                click.secho(f"  Could not read logs: {e.reason}", fg="red")

if __name__ == '__main__':
    main()
```

### Step 3: Test the Diagnostic Script
```bash
# Run help command to see click configurations
python diagnose.py --help

# Audit default namespace
python diagnose.py --namespace default
```

---

## 🔒 Security Considerations
1. **Sanitize CLI Inputs**: When parsing inputs (such as names or namespaces) in scripts that execute local shell commands (`subprocess.run`), validate inputs strictly to prevent **command injection** vulnerabilities.
2. **Kubeconfig Access**: Run scripts using the minimum necessary RBAC permissions. Never build custom monitoring integrations using the cluster-admin `ServiceAccount`.
3. **Handle Tokens Safely**: Access credentials (like HuggingFace/Database tokens) must be injected via OS Environment Variables (`os.environ.get`) rather than hardcoded in the scripts.

---

## 📈 Scaling & Observability Considerations
* **Paging API Queries**: When managing large enterprise clusters with 10,000+ pods, querying them all in one go will overload the API server. Use the `limit` and `continue` pagination options in your client API queries.
* **Structured Logging**: Standardize script outputs using the Python `logging` library with a JSON formatter, allowing platforms like Loki or ElasticSearch to parse them automatically.

---

## 🔍 Troubleshooting Guide

### 💥 Issue: `kubernetes.config.config_exception.ConfigException: No kube-config file found.`
* **Root Cause**: The automation script cannot locate your `.kube/config` file, or has been executed inside an environment lacking Kubernetes credentials.
* **Diagnostic Check**:
  ```bash
  # Check if standard config file exists in your home directory
  ls ~/.kube/config
  ```
* **Mitigation**:
  1. Ensure you have run local authentication commands for your target cluster (e.g. `gcloud container clusters get-credentials` or `aws eks update-kubeconfig`).
  2. Set the environment variable `KUBECONFIG` to point explicitly to your config file path.
  3. Ensure the script has read permissions for the config file.

---

## 🌟 Best Practices & Open-Source Tools
* **Click**: Use Click to build powerful command-line interfaces in Python with automatic help menus and option parsing.
* **Httpx**: Use `httpx` to replace `requests` for fast, asynchronous HTTP network calls.
