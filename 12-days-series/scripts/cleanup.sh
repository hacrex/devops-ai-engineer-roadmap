#!/bin/bash

# Cleanup script to remove temporary files and caches
# Run this to free up disk space

set -e

echo "=========================================="
echo "Cleanup Utility"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

cleanup_python() {
    echo -e "${YELLOW}Cleaning Python caches...${NC}"
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete 2>/dev/null || true
    find . -type f -name "*.pyo" -delete 2>/dev/null || true
    find . -type f -name "*.pyd" -delete 2>/dev/null || true
    find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
    echo -e "${GREEN}✓ Python caches cleaned${NC}"
}

cleanup_test() {
    echo -e "${YELLOW}Cleaning test artifacts...${NC}"
    find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name ".coverage" -delete 2>/dev/null || true
    find . -type f -name "coverage.xml" -delete 2>/dev/null || true
    echo -e "${GREEN}✓ Test artifacts cleaned${NC}"
}

cleanup_build() {
    echo -e "${YELLOW}Cleaning build directories...${NC}"
    find . -type d -name "build" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name "*.egg" -exec rm -rf {} + 2>/dev/null || true
    echo -e "${GREEN}✓ Build directories cleaned${NC}"
}

cleanup_docker() {
    if command -v docker &> /dev/null && docker info &> /dev/null; then
        echo -e "${YELLOW}Cleaning Docker (unused resources)...${NC}"
        docker system prune -f --volumes
        echo -e "${GREEN}✓ Docker cleaned${NC}"
    else
        echo -e "${YELLOW}⚠ Docker not available, skipping${NC}"
    fi
}

cleanup_models() {
    echo -e "${YELLOW}Cleaning model caches (optional)...${NC}"
    echo "This will remove downloaded models from Hugging Face cache."
    read -p "Continue? (y/N): " confirm
    if [[ $confirm =~ ^[Yy]$ ]]; then
        rm -rf ~/.cache/huggingface/hub
        echo -e "${GREEN}✓ Model cache cleaned${NC}"
    else
        echo "Skipped model cache cleanup"
    fi
}

cleanup_venv() {
    echo -e "${YELLOW}Virtual environment cleanup (optional)...${NC}"
    echo "This will remove the venv directory."
    read -p "Continue? (y/N): " confirm
    if [[ $confirm =~ ^[Yy]$ ]]; then
        rm -rf venv
        echo -e "${GREEN}✓ Virtual environment removed${NC}"
    else
        echo "Skipped venv cleanup"
    fi
}

show_disk_usage() {
    echo ""
    echo -e "${GREEN}Current disk usage:${NC}"
    df -h . | tail -n 1
}

# Main cleanup
main() {
    echo "Starting cleanup..."
    echo ""
    
    cleanup_python
    cleanup_test
    cleanup_build
    
    echo ""
    echo "Optional cleanups:"
    echo "1. Docker cleanup (removes unused containers/images)"
    echo "2. Model cache cleanup (frees several GBs)"
    echo "3. Virtual environment removal"
    echo ""
    read -p "Run optional cleanups? (y/N): " run_optional
    
    if [[ $run_optional =~ ^[Yy]$ ]]; then
        cleanup_docker
        cleanup_models
        cleanup_venv
    fi
    
    echo ""
    show_disk_usage
    
    echo ""
    echo -e "${GREEN}=========================================="
    echo "Cleanup complete! 🎉"
    echo -e "${GREEN}==========================================${NC}"
}

# Run main function
main "$@"
