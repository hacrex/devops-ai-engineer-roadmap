#!/bin/bash

# 12 Days of AI Infrastructure - Setup Script
# This script sets up the development environment for all 12 days

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running on supported OS
check_os() {
    log_info "Checking operating system..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
        log_info "Detected Linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
        log_info "Detected macOS"
    else
        log_warning "Unsupported OS: $OSTYPE. Some features may not work."
        OS="unknown"
    fi
}

# Check Python version
check_python() {
    log_info "Checking Python version..."
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        log_info "Python version: $PYTHON_VERSION"
        
        # Check if Python >= 3.9
        if [[ $(python3 -c "import sys; print(sys.version_info >= (3, 9))") == "True" ]]; then
            PYTHON_CMD="python3"
            log_success "Python 3.9+ detected"
        else
            log_error "Python 3.9+ required. Found: $PYTHON_VERSION"
            exit 1
        fi
    else
        log_error "Python3 not found. Please install Python 3.9 or higher."
        exit 1
    fi
}

# Check Docker
check_docker() {
    log_info "Checking Docker..."
    if command -v docker &> /dev/null; then
        if docker info &> /dev/null; then
            DOCKER_VERSION=$(docker --version)
            log_success "Docker detected: $DOCKER_VERSION"
            DOCKER_AVAILABLE=true
        else
            log_warning "Docker installed but daemon not running"
            DOCKER_AVAILABLE=false
        fi
    else
        log_warning "Docker not found. Container examples will be skipped."
        DOCKER_AVAILABLE=false
    fi
}

# Check kubectl
check_kubectl() {
    log_info "Checking kubectl..."
    if command -v kubectl &> /dev/null; then
        KUBECTL_VERSION=$(kubectl version --client --short 2>/dev/null || kubectl version --client)
        log_success "kubectl detected: $KUBECTL_VERSION"
        KUBECTL_AVAILABLE=true
    else
        log_warning "kubectl not found. Kubernetes examples will be limited."
        KUBECTL_AVAILABLE=false
    fi
}

# Check Ollama
check_ollama() {
    log_info "Checking Ollama..."
    if command -v ollama &> /dev/null; then
        OLLAMA_VERSION=$(ollama --version)
        log_success "Ollama detected: $OLLAMA_VERSION"
        OLLAMA_AVAILABLE=true
    else
        log_warning "Ollama not found. Local LLM examples will require manual installation."
        OLLAMA_AVAILABLE=false
    fi
}

# Create virtual environment
setup_venv() {
    log_info "Setting up Python virtual environment..."
    
    if [ -d "venv" ]; then
        log_warning "Virtual environment already exists. Removing..."
        rm -rf venv
    fi
    
    $PYTHON_CMD -m venv venv
    log_success "Virtual environment created"
    
    # Activate venv
    source venv/bin/activate
    log_success "Virtual environment activated"
    
    # Upgrade pip
    log_info "Upgrading pip..."
    pip install --upgrade pip
}

# Install base requirements
install_base_requirements() {
    log_info "Installing base requirements..."
    
    cat > requirements-base.txt << EOF
# Core dependencies for all days
requests>=2.31.0
python-dotenv>=1.0.0
pyyaml>=6.0
tqdm>=4.65.0
EOF
    
    pip install -r requirements-base.txt
    log_success "Base requirements installed"
}

# Install Day-specific requirements
install_day_requirements() {
    log_info "Installing day-specific requirements..."
    
    # Day 01-03: Containers & Automation
    cat > requirements-days-01-03.txt << EOF
docker>=6.0.0
kubernetes>=28.0.0
paramiko>=3.3.0
fabric>=3.2.0
EOF
    
    # Day 04-06: Prompt Engineering & Local LLMs
    cat > requirements-days-04-06.txt << EOF
openai>=1.0.0
anthropic>=0.7.0
transformers>=4.35.0
torch>=2.0.0
accelerate>=0.24.0
sentencepiece>=0.1.99
protobuf>=4.25.0
EOF
    
    # Day 07-09: K8s AI & RAG
    cat > requirements-days-07-09.txt << EOF
chromadb>=0.4.0
langchain>=0.1.0
langchain-community>=0.0.10
faiss-cpu>=1.7.4
pinecone-client>=3.0.0
llama-index>=0.9.0
EOF
    
    # Day 10-12: Observability, Security, Projects
    cat > requirements-days-10-12.txt << EOF
prometheus-client>=0.19.0
grafana-api>=1.0.0
guardrails-ai>=0.3.0
mlflow>=2.9.0
wandb>=0.16.0
pytest>=7.4.0
EOF
    
    # Install all
    pip install -r requirements-days-01-03.txt
    pip install -r requirements-days-04-06.txt
    pip install -r requirements-days-07-09.txt
    pip install -r requirements-days-10-12.txt
    
    log_success "All day-specific requirements installed"
}

# Create .env file template
create_env_template() {
    log_info "Creating .env template..."
    
    cat > .env.example << EOF
# API Keys (Get these from respective providers)
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
HUGGINGFACE_TOKEN=your_hf_token_here

# Vector Database
CHROMA_DB_PATH=./chroma_db
PINECONE_API_KEY=your_pinecone_key_here

# Monitoring
GRAFANA_URL=http://localhost:3000
PROMETHEUS_URL=http://localhost:9090

# Optional: Proxy settings
# HTTP_PROXY=http://proxy:port
# HTTPS_PROXY=http://proxy:port
EOF
    
    if [ ! -f ".env" ]; then
        cp .env.example .env
        log_warning "Please update .env with your API keys"
    else
        log_info ".env file already exists"
    fi
}

# Setup Docker containers (optional)
setup_docker_containers() {
    if [ "$DOCKER_AVAILABLE" = false ]; then
        log_warning "Skipping Docker setup - Docker not available"
        return
    fi
    
    log_info "Setting up Docker containers..."
    
    # Create docker-compose.yml
    cat > docker-compose.yml << EOF
version: '3.8'

services:
  # ChromaDB for vector storage
  chromadb:
    image: chromadb/chroma:latest
    ports:
      - "8000:8000"
    volumes:
      - ./chroma_data:/chroma/chroma
    environment:
      - CHROMA_DB_IMPL=chromadb.db.impl.sqlite
  
  # Prometheus for monitoring
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
  
  # Grafana for visualization
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_USERS_ALLOW_SIGN_UP=false
    depends_on:
      - prometheus
  
  # Local LLM server (Ollama alternative)
  vllm:
    image: vllm/vllm-openai:latest
    ports:
      - "8001:8000"
    volumes:
      - ./models:/models
    environment:
      - HUGGING_FACE_HUB_TOKEN=\${HUGGINGFACE_TOKEN}
    command: >
      --model meta-llama/Llama-2-7b-chat-hf
      --download-dir /models
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

volumes:
  prometheus_data:
  grafana_data:
EOF
    
    log_success "Docker Compose configuration created"
    log_info "To start services: docker-compose up -d"
}

# Create monitoring configuration
setup_monitoring() {
    log_info "Setting up monitoring configuration..."
    
    mkdir -p monitoring
    
    cat > monitoring/prometheus.yml << EOF
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
  
  - job_name: 'api-server'
    static_configs:
      - targets: ['host.docker.internal:8000']
    metrics_path: '/metrics'
EOF
    
    log_success "Prometheus configuration created"
}

# Create helper scripts
create_helper_scripts() {
    log_info "Creating helper scripts..."
    
    mkdir -p scripts
    
    # Download models script
    cat > scripts/download_models.sh << 'SCRIPT'
#!/bin/bash
# Download commonly used models

echo "Downloading models..."

# Create models directory
mkdir -p models

# Pull Ollama models (if Ollama is available)
if command -v ollama &> /dev/null; then
    echo "Pulling small model for testing..."
    ollama pull llama3.2:1b
    echo "Model download complete"
else
    echo "Ollama not found. Skipping model download."
fi
SCRIPT
    
    chmod +x scripts/download_models.sh
    
    # Clean up script
    cat > scripts/cleanup.sh << 'SCRIPT'
#!/bin/bash
# Clean up temporary files and caches

echo "Cleaning up..."

# Remove Python caches
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Remove venv (optional)
# rm -rf venv

# Clean Docker
# docker system prune -a

# Clean Hugging Face cache
# rm -rf ~/.cache/huggingface

echo "Cleanup complete"
SCRIPT
    
    chmod +x scripts/cleanup.sh
    
    log_success "Helper scripts created"
}

# Print next steps
print_next_steps() {
    echo ""
    log_success "Setup complete! 🎉"
    echo ""
    echo "=========================================="
    echo "Next Steps:"
    echo "=========================================="
    echo ""
    echo "1. Activate virtual environment:"
    echo "   source venv/bin/activate"
    echo ""
    echo "2. Configure API keys:"
    echo "   Edit .env file with your API keys"
    echo ""
    if [ "$DOCKER_AVAILABLE" = true ]; then
        echo "3. Start supporting services (optional):"
        echo "   docker-compose up -d"
        echo ""
    fi
    echo "3. Start with Day 01:"
    echo "   cd day01-linux-containers"
    echo "   cat README.md"
    echo ""
    echo "4. Check system requirements:"
    echo "   ./scripts/check_system.sh (if available)"
    echo ""
    echo "=========================================="
    echo "Resources:"
    echo "=========================================="
    echo "- Troubleshooting: TROUBLESHOOTING.md"
    echo "- Contributing: CONTRIBUTING.md"
    echo "- Main README: README.md"
    echo ""
    echo "Happy learning! 🚀"
    echo ""
}

# Main setup function
main() {
    echo "=========================================="
    echo "12 Days of AI Infrastructure - Setup"
    echo "=========================================="
    echo ""
    
    # Run checks
    check_os
    check_python
    check_docker
    check_kubectl
    check_ollama
    
    echo ""
    
    # Setup environment
    setup_venv
    install_base_requirements
    install_day_requirements
    create_env_template
    
    # Optional setups
    setup_docker_containers
    setup_monitoring
    create_helper_scripts
    
    # Print summary
    print_next_steps
}

# Run main function
main "$@"
