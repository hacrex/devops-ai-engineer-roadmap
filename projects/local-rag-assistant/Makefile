.PHONY: install test lint clean run docker-up docker-down help

# Default target
help:
	@echo "Local RAG Assistant - Available Commands"
	@echo ""
	@echo "  make install      Install dependencies"
	@echo "  make test         Run tests"
	@echo "  make lint         Run linter"
	@echo "  make clean        Clean up files"
	@echo "  make run          Start Streamlit app"
	@echo "  make docker-up    Start all services with Docker Compose"
	@echo "  make docker-down  Stop all Docker services"
	@echo ""

install:
	pip install -r requirements.txt

test:
	pytest tests/ -v --cov=app --cov-report=term-missing

lint:
	flake8 app.py --max-line-length=100
	black --check app.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache .coverage htmlcov/
	rm -rf qdrant_storage/

run:
	@echo "Starting Qdrant (ensure Docker is running)..."
	docker run -d -p 6333:6333 -p 6334:6334 --name qdrant qdrant/qdrant || echo "Qdrant may already be running"
	@echo ""
	@echo "Starting Streamlit app..."
	streamlit run app.py

docker-up:
	docker-compose up -d
	@echo ""
	@echo "Services started! Access Streamlit at http://localhost:8501"
	@echo "Qdrant dashboard at http://localhost:6333/dashboard"

docker-down:
	docker-compose down

check-services:
	@echo "=== Service Status Check ==="
	@echo ""
	@echo "Qdrant:"
	curl -s http://localhost:6333/ | head -3 || echo "Not running"
	@echo ""
	@echo "Ollama:"
	curl -s http://localhost:11434/api/tags | head -5 || echo "Not running"
	@echo ""
	@echo "Docker containers:"
	docker ps | grep -E "(qdrant|rag)" || echo "No containers running"
