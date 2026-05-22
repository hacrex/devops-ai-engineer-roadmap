.PHONY: install test lint clean run help

# Default target
help:
	@echo "DevOps AI Copilot - Available Commands"
	@echo ""
	@echo "  make install    Install dependencies"
	@echo "  make test       Run tests"
	@echo "  make lint       Run linter"
	@echo "  make clean      Clean up files"
	@echo "  make run        Run the copilot CLI"
	@echo ""

install:
	pip install -r requirements.txt

test:
	pytest tests/ -v --cov=copilot --cov-report=term-missing

lint:
	flake8 copilot.py --max-line-length=100
	black --check copilot.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache .coverage htmlcov/

run:
	@echo "Ensure Ollama is running: ollama serve &"
	@echo ""
	python copilot.py --help

generate-k8s:
	python copilot.py generate kubernetes --prompt "nginx deployment with 3 replicas"

generate-terraform:
	python copilot.py generate terraform --prompt "AWS S3 bucket with versioning"

check-system:
	@echo "=== System Check ==="
	@echo "Python version:"
	python --version
	@echo ""
	@echo "Ollama status:"
	curl -s http://localhost:11434/api/tags | head -5 || echo "Ollama not running"
	@echo ""
	@echo "Available models:"
	ollama list 2>/dev/null || echo "Ollama not installed"
