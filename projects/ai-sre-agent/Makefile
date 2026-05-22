.PHONY: install test lint clean run help

help:
	@echo "AI SRE Agent - Available Commands"
	@echo ""
	@echo "  make install    Install dependencies"
	@echo "  make test       Run tests"
	@echo "  make lint       Run linter"
	@echo "  make clean      Clean up files"
	@echo "  make run        Start Flask server"
	@echo ""

install:
	pip install -r requirements.txt

test:
	pytest tests/ -v --cov=sre_agent --cov-report=term-missing

lint:
	flake8 sre_agent.py --max-line-length=100
	black --check sre_agent.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage htmlcov/

run:
	export FLASK_APP=sre_agent.py && flask run --host=0.0.0.0 --port=5000

check-k8s:
	@echo "=== Kubernetes Connection Check ==="
	kubectl cluster-info || echo "Kubernetes not accessible"
	kubectl get nodes || echo "Cannot get nodes"
