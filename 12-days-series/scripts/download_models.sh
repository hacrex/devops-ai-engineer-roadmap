#!/bin/bash

# Helper script to download models for local testing
# Used in Day 05 (Local LLMs) and Day 07 (AI Inference)

set -e

echo "=========================================="
echo "Model Download Helper"
echo "=========================================="
echo ""

# Check if Ollama is available
if command -v ollama &> /dev/null; then
    echo "✓ Ollama detected"
    echo ""
    
    echo "Pulling recommended models for learning..."
    echo ""
    
    # Small model for quick testing
    echo "1. Pulling llama3.2:1b (small, fast)..."
    ollama pull llama3.2:1b
    
    # Medium model for better quality
    echo "2. Pulling llama3.2:3b (medium, balanced)..."
    ollama pull llama3.2:3b
    
    # Embedding model
    echo "3. Pulling nomic-embed-text (for RAG)..."
    ollama pull nomic-embed-text
    
    echo ""
    echo "✓ All models downloaded successfully!"
    echo ""
    echo "Available models:"
    ollama list
else
    echo "⚠ Ollama not found"
    echo ""
    echo "To install Ollama:"
    echo "  - Linux/Mac: curl -fsSL https://ollama.com/install.sh | sh"
    echo "  - Windows: Download from https://ollama.com/download"
    echo ""
    echo "Then run this script again."
fi

echo ""
echo "=========================================="
echo "Alternative: Hugging Face Models"
echo "=========================================="
echo ""

if command -v huggingface-cli &> /dev/null; then
    echo "Hugging Face CLI detected"
    echo ""
    echo "To download models manually:"
    echo "  huggingface-cli download meta-llama/Llama-2-7b-chat-hf"
    echo "  huggingface-cli download sentence-transformers/all-MiniLM-L6-v2"
else
    echo "Install Hugging Face CLI:"
    echo "  pip install huggingface_hub"
fi

echo ""
echo "Done! 🎉"
