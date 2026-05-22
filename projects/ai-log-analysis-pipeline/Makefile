.PHONY: install test lint clean run docker-up help

help:
	@echo "AI Log Analysis Pipeline - Available Commands"
	@echo ""
	@echo "  make install    Install dependencies"
	@echo "  make test       Run tests"
	@echo "  make lint       Run linter"
	@echo "  make clean      Clean up files"
	@echo "  make run        Start FastAPI server"
	@echo "  make docker-up  Start with Docker Compose"
	@echo ""

install:
	pip install -r requirements.txt

test:
	pytest tests/ -v --cov=analyzer --cov-report=term-missing

lint:
	flake8 analyzer.py --max-line-length=100
	black --check analyzer.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage htmlcov/

run:
	uvicorn analyzer:app --host 0.0.0.0 --port 8000 --reload

docker-up:
	docker-compose up -d
	@echo "API running at http://localhost:8000"
	@echo "Docs at http://localhost:8000/docs"
