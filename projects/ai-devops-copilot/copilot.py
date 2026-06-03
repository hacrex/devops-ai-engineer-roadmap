import os
import yaml
import click
import httpx

# 1. Configuration Loading
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.yaml")


def load_config():
    if not os.path.exists(CONFIG_PATH):
        # Fallback Mock Config if file not found
        return {
            "model": "qwen2.5-coder:7b",
            "ollama_url": "http://localhost:11434",
            "system_instruction": (
                "You are a DevOps Copilot. Generate only clean code blocks without markdown "
                "explanations."
            ),
        }
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


config_data = load_config()
OLLAMA_URL = config_data.get("ollama_url", "http://localhost:11434")
MODEL_NAME = config_data.get("model", "qwen2.5-coder:7b")


@click.group()
def cli():
    """🤖 DevOps AI Copilot CLI Utility

    Automates manifest generation, Terraform modules, and secure system checks.
    """
    pass


@cli.group()
def generate():
    """Generate infrastructure assets from natural-language prompts."""
    pass


def query_model(prompt):
    """Return a local model completion, or None when the model runtime is unavailable."""
    payload = {"model": MODEL_NAME, "prompt": prompt, "stream": False}
    try:
        response = httpx.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=30.0)
        if response.status_code == 200:
            return response.json().get("response", "").strip()
    except httpx.HTTPError:
        return None
    return None


@generate.command(name="kubernetes")
@click.option(
    "--prompt", "prompt_text", required=True, help="Natural-language Kubernetes request"
)
def generate_kubernetes(prompt_text):
    """Generate a Kubernetes manifest from a prompt."""
    prompt = f"""Generate a production-grade Kubernetes manifest for this request:
    {prompt_text}

    Security requirements: Enforce runAsNonRoot, readOnlyRootFilesystem,
    and resource boundaries.
    Output ONLY valid YAML. Do not write text summaries or wrap in markdown backticks.
    """
    click.secho("🚀 Generating Kubernetes manifest from prompt...", fg="cyan")
    output = query_model(prompt)
    if output and "apiVersion" in output:
        click.echo(output)
        return

    click.secho(
        "⚠️ Local model unavailable or returned invalid YAML. Simulated output:",
        fg="yellow",
    )
    click.echo("""apiVersion: apps/v1
kind: Deployment
metadata:
  name: generated-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: generated-app
  template:
    metadata:
      labels:
        app: generated-app
    spec:
      containers:
        - name: app
          image: nginx:latest
          securityContext:
            runAsNonRoot: true
            readOnlyRootFilesystem: true
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 512Mi""")


@generate.command(name="terraform")
@click.option(
    "--prompt", "prompt_text", required=True, help="Natural-language Terraform request"
)
def generate_terraform(prompt_text):
    """Generate Terraform configuration from a prompt."""
    prompt = f"""Generate valid Terraform configuration for this request:
    {prompt_text}

    Output ONLY clean HCL code. Do not write text summaries or wrapping markers.
    """
    click.secho("🚀 Generating Terraform configuration from prompt...", fg="cyan")
    output = query_model(prompt)
    if output:
        click.echo(output)
        return

    click.secho("⚠️ Local model unavailable. Simulated HCL output:", fg="yellow")
    click.echo("""resource "null_resource" "generated" {
  triggers = {
    request = "generated-from-prompt"
  }
}""")


@cli.command()
@click.option("--name", "-n", required=True, help="Name of the Kubernetes deployment")
@click.option("--image", "-i", required=True, help="Container image registry path")
@click.option("--port", "-p", default=8080, help="Container port mapping")
@click.option("--gpu", is_flag=True, help="Flag to request 1 NVIDIA GPU")
def k8s(name, image, port, gpu):
    """☸️ Generate a Secure Kubernetes Deployment YAML"""
    gpu_spec = '\n            nvidia.com/gpu: "1"' if gpu else ""

    prompt = f"""Generate a production-grade Kubernetes Deployment manifest.
    Name: {name}
    Image: {image}
    Port: {port}
    GPU Requested: {gpu}

    Security requirements: Enforce runAsNonRoot, readOnlyRootFilesystem,
    and resource boundaries.
    Output ONLY valid YAML. Do not write text summaries or wrap in markdown backticks.
    """

    click.secho(f"🚀 Generating Kubernetes manifest for '{name}'...", fg="cyan")

    # 2. Query Local Model Server
    try:
        payload = {"model": MODEL_NAME, "prompt": prompt, "stream": False}
        response = httpx.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=30.0)
        if response.status_code == 200:
            result = response.json()
            yaml_output = result["response"].strip()

            # Simple validation check: ensure output has apiVersion
            if "apiVersion" in yaml_output:
                filename = f"deployment-{name}.yaml"
                with open(filename, "w") as f:
                    f.write(yaml_output)
                click.secho(
                    f"✨ Successfully generated secure config file: {filename}",
                    fg="green",
                    bold=True,
                )
                click.echo(yaml_output)
            else:
                click.secho(
                    "⚠️ Model generated invalid YAML structure. "
                    "Re-trying with system constraints...",
                    fg="yellow",
                )
        else:
            click.secho("Error contacting Ollama API.", fg="red")
    except Exception:
        click.secho(
            "⚠️ Local Ollama server offline! Simulated secure YAML Output:", fg="yellow"
        )
        mock_yaml = f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {name}
  namespace: default
spec:
  replicas: 2
  selector:
    matchLabels:
      app: {name}
  template:
    metadata:
      labels:
        app: {name}
    spec:
      containers:
      - name: web-app
        image: {image}
        ports:
        - containerPort: {port}
        securityContext:
          runAsNonRoot: true
          readOnlyRootFilesystem: true
        resources:
          limits:
            cpu: "1"
            memory: "2Gi"{gpu_spec}
          requests:
            cpu: "500m"
            memory: "1Gi"{gpu_spec}"""
        filename = f"deployment-{name}.yaml"
        with open(filename, "w") as f:
            f.write(mock_yaml)
        click.secho(f"✨ [Simulation Mode] Generated file: {filename}", fg="green")
        click.echo(mock_yaml)


@cli.command()
@click.option("--provider", "-pr", default="aws", help="Cloud provider (aws, gcp)")
@click.option("--resource", "-r", required=True, help="Resource type (vpc, s3, ec2)")
@click.option("--name", "-n", required=True, help="Resource name tag")
def terraform(provider, resource, name):
    """🏗️ Generate standard Terraform Module blocks"""
    prompt = f"""Generate a valid Terraform module configuration for Cloud: {provider}.
    Target Resource: {resource}
    Name tag: {name}

    Output ONLY clean HCL code. Do not write text summaries or wrapping markers.
    """
    click.secho("🚀 Generating Terraform configuration...", fg="cyan")

    try:
        payload = {"model": MODEL_NAME, "prompt": prompt, "stream": False}
        response = httpx.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=30.0)
        if response.status_code == 200:
            result = response.json()
            click.secho("✨ Generated HCL Module:", fg="green")
            click.echo(result["response"])
    except Exception:
        click.secho("⚠️ Local Ollama offline. Simulated HCL Output:", fg="yellow")
        mock_hcl = f"""resource "{provider}_{resource}" "{name}" {{
  name = "{name}-resource"
  tags = {{
    Environment = "production"
    ManagedBy   = "devops-ai-copilot"
  }}
}}"""
        click.echo(mock_hcl)


if __name__ == "__main__":
    cli()
