#!/usr/bin/env python3
"""
Local LLM Inference Examples
Demonstrates running LLMs locally with Ollama, llama.cpp, and vLLM.
"""

import os
import json
import time
from typing import List, Dict, Generator

# =============================================================================
# 1. OLLAMA INFERENCE
# =============================================================================

def ollama_basic_completion(model: str = "llama3.2", prompt: str = "") -> str:
    """
    Basic completion using Ollama API.
    Requires Ollama running locally (default: http://localhost:11434)
    """
    import requests
    
    if not prompt:
        prompt = "Explain quantum computing in one paragraph."
    
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9,
            "num_predict": 512
        }
    }
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        return result.get("response", "")
    except requests.exceptions.ConnectionError:
        return "Error: Ollama not running. Start with: ollama serve"
    except Exception as e:
        return f"Error: {str(e)}"


def ollama_chat_completion(model: str = "llama3.2", messages: List[Dict] = None) -> str:
    """
    Chat completion using Ollama API with conversation history.
    """
    import requests
    
    if messages is None:
        messages = [
            {"role": "system", "content": "You are a helpful coding assistant."},
            {"role": "user", "content": "Write a Python function to calculate fibonacci numbers."}
        ]
    
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9
        }
    }
    
    try:
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        result = response.json()
        return result["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"


def ollama_streaming_response(model: str = "llama3.2", prompt: str = "") -> Generator[str, None, None]:
    """
    Stream responses from Ollama for real-time output.
    """
    import requests
    
    if not prompt:
        prompt = "Tell me a short story about a robot learning to paint."
    
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": True,
        "options": {
            "temperature": 0.8,
            "top_p": 0.95
        }
    }
    
    try:
        response = requests.post(url, json=payload, stream=True, timeout=120)
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                yield data.get("response", "")
                if data.get("done", False):
                    break
    except Exception as e:
        yield f"Error: {str(e)}"


# =============================================================================
# 2. LLAMA.CPP INFERENCE
# =============================================================================

def llama_cpp_basic(model_path: str = "", prompt: str = "") -> str:
    """
    Basic inference using llama-cpp-python.
    Requires: pip install llama-cpp-python
    """
    try:
        from llama_cpp import Llama
    except ImportError:
        return "Error: Install llama-cpp-python first: pip install llama-cpp-python"
    
    if not model_path:
        return "Error: Provide path to GGUF model file"
    
    if not os.path.exists(model_path):
        return f"Error: Model file not found at {model_path}"
    
    try:
        # Load model
        llm = Llama(
            model_path=model_path,
            n_ctx=4096,
            n_threads=4,
            verbose=False
        )
        
        # Generate completion
        output = llm(
            prompt,
            max_tokens=512,
            temperature=0.7,
            top_p=0.9,
            stop=["User:", "\n\n"],
            echo=False
        )
        
        return output["choices"][0]["text"]
    
    except Exception as e:
        return f"Error: {str(e)}"


def llama_cpp_with_gpu(model_path: str = "", gpu_layers: int = 35) -> str:
    """
    GPU-accelerated inference using llama-cpp-python.
    """
    try:
        from llama_cpp import Llama
    except ImportError:
        return "Error: Install llama-cpp-python first"
    
    if not model_path:
        return "Error: Provide path to GGUF model file"
    
    try:
        llm = Llama(
            model_path=model_path,
            n_ctx=4096,
            n_gpu_layers=gpu_layers,  # Offload layers to GPU
            n_threads=4,
            verbose=False
        )
        
        prompt = "What are the advantages of running LLMs locally?"
        output = llm(prompt, max_tokens=256, temperature=0.7, echo=False)
        
        return output["choices"][0]["text"]
    
    except Exception as e:
        return f"Error: {str(e)}"


# =============================================================================
# 3. VLLM INFERENCE (HIGH PERFORMANCE)
# =============================================================================

def vllm_basic_inference(model_name: str = "meta-llama/Llama-2-7b-chat-hf") -> str:
    """
    High-performance inference using vLLM.
    Requires: pip install vllm
    """
    try:
        from vllm import LLM, SamplingParams
    except ImportError:
        return "Error: Install vLLM first: pip install vllm"
    
    try:
        # Initialize LLM
        llm = LLM(
            model=model_name,
            trust_remote_code=True,
            tensor_parallel_size=1  # Number of GPUs
        )
        
        # Sampling parameters
        sampling_params = SamplingParams(
            temperature=0.7,
            top_p=0.9,
            max_tokens=512,
            stop=["</s>", "User:"]
        )
        
        # Prompts
        prompts = [
            "Explain the concept of containerization in DevOps.",
            "What is the difference between Kubernetes and Docker Swarm?",
            "How does CI/CD improve software development?"
        ]
        
        # Generate outputs
        outputs = llm.generate(prompts, sampling_params)
        
        results = []
        for output in outputs:
            results.append({
                "prompt": output.prompt,
                "generated_text": output.outputs[0].text,
                "tokens_generated": len(output.outputs[0].token_ids)
            })
        
        return json.dumps(results, indent=2)
    
    except Exception as e:
        return f"Error: {str(e)}"


def vllm_openai_compatible_server():
    """
    Start vLLM's OpenAI-compatible API server.
    Run this as a separate process.
    """
    print("""
To start vLLM OpenAI-compatible server:

python -m vllm.entrypoints.openai.api_server \\
    --model meta-llama/Llama-2-7b-chat-hf \\
    --host 0.0.0.0 \\
    --port 8000

Then query it like OpenAI API:

curl http://localhost:8000/v1/completions \\
    -H "Content-Type: application/json" \\
    -d '{
        "model": "meta-llama/Llama-2-7b-chat-hf",
        "prompt": "Hello, my name is",
        "max_tokens": 100
    }'
""")


# =============================================================================
# 4. MODEL QUANTIZATION COMPARISON
# =============================================================================

def compare_quantization_levels():
    """
    Compare different quantization levels for local models.
    """
    comparison = {
        "FP16": {
            "size": "~14GB for 7B model",
            "quality": "Best",
            "speed": "Fast on GPU",
            "ram_required": "16GB+"
        },
        "Q8_0": {
            "size": "~7GB for 7B model", 
            "quality": "Excellent",
            "speed": "Very fast",
            "ram_required": "8GB+"
        },
        "Q4_K_M": {
            "size": "~4GB for 7B model",
            "quality": "Very good",
            "speed": "Fastest",
            "ram_required": "6GB+"
        },
        "Q2_K": {
            "size": "~3GB for 7B model",
            "quality": "Good",
            "speed": "Fast",
            "ram_required": "4GB+"
        }
    }
    
    print("=" * 70)
    print("QUANTIZATION LEVEL COMPARISON")
    print("=" * 70)
    print(f"{'Level':<10} {'Size':<20} {'Quality':<12} {'Speed':<12} {'RAM':<10}")
    print("-" * 70)
    
    for level, info in comparison.items():
        print(f"{level:<10} {info['size']:<20} {info['quality']:<12} {info['speed']:<12} {info['ram_required']:<10}")
    
    print("\nRecommendation: Use Q4_K_M for best balance of quality and performance")


# =============================================================================
# 5. BATCH PROCESSING
# =============================================================================

def batch_processing_ollama(prompts: List[str], model: str = "llama3.2") -> List[str]:
    """
    Process multiple prompts in batch using Ollama.
    """
    import requests
    
    results = []
    url = "http://localhost:11434/api/generate"
    
    for prompt in prompts:
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.7}
        }
        
        try:
            response = requests.post(url, json=payload, timeout=60)
            result = response.json()
            results.append(result.get("response", ""))
        except Exception as e:
            results.append(f"Error: {str(e)}")
    
    return results


def batch_processing_with_concurrency(prompts: List[str], model: str = "llama3.2", max_workers: int = 4) -> List[str]:
    """
    Process prompts concurrently for better throughput.
    """
    import requests
    from concurrent.futures import ThreadPoolExecutor, as_completed
    
    def process_single_prompt(prompt: str) -> str:
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.7}
        }
        
        try:
            response = requests.post(url, json=payload, timeout=60)
            return response.json().get("response", "")
        except Exception as e:
            return f"Error: {str(e)}"
    
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_single_prompt, p): i for i, p in enumerate(prompts)}
        
        for future in as_completed(futures):
            results.append(future.result())
    
    return results


# =============================================================================
# 6. PERFORMANCE MONITORING
# =============================================================================

def benchmark_inference(model: str = "llama3.2", num_runs: int = 5):
    """
    Benchmark inference speed and token generation.
    """
    import requests
    
    prompt = "Explain the benefits of microservices architecture in modern software development."
    url = "http://localhost:11434/api/generate"
    
    print(f"\nBenchmarking {model} with {num_runs} runs...")
    print("=" * 70)
    
    times = []
    tokens_per_second = []
    
    for i in range(num_runs):
        start_time = time.time()
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.7}
        }
        
        try:
            response = requests.post(url, json=payload, timeout=120)
            end_time = time.time()
            
            result = response.json()
            elapsed = end_time - start_time
            tokens = result.get("eval_count", 0)
            
            times.append(elapsed)
            tps = tokens / elapsed if elapsed > 0 else 0
            tokens_per_second.append(tps)
            
            print(f"Run {i+1}: {elapsed:.2f}s | Tokens: {tokens} | TPS: {tps:.2f}")
            
        except Exception as e:
            print(f"Run {i+1}: Error - {str(e)}")
    
    if times:
        print("\n" + "=" * 70)
        print(f"Average Time: {sum(times)/len(times):.2f}s")
        print(f"Average TPS: {sum(tokens_per_second)/len(tokens_per_second):.2f}")
        print(f"Min TPS: {min(tokens_per_second):.2f}")
        print(f"Max TPS: {max(tokens_per_second):.2f}")


# =============================================================================
# MAIN DEMONSTRATION
# =============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("LOCAL LLM INFERENCE EXAMPLES")
    print("=" * 80)
    
    # Example 1: Ollama basic completion
    print("\n1. OLLAMA BASIC COMPLETION")
    print("-" * 40)
    print("Note: Requires Ollama running on localhost:11434")
    # Uncomment to test:
    # result = ollama_basic_completion()
    # print(result)
    
    # Example 2: Ollama chat
    print("\n2. OLLAMA CHAT COMPLETION")
    print("-" * 40)
    # messages = [
    #     {"role": "system", "content": "You are a helpful assistant."},
    #     {"role": "user", "content": "What is 2 + 2?"}
    # ]
    # result = ollama_chat_completion(messages=messages)
    # print(result)
    
    # Example 3: Quantization comparison
    print("\n3. QUANTIZATION LEVELS")
    print("-" * 40)
    compare_quantization_levels()
    
    # Example 4: Performance benchmark
    print("\n4. PERFORMANCE BENCHMARK")
    print("-" * 40)
    print("Note: Requires Ollama running")
    # benchmark_inference(num_runs=3)
    
    # Example 5: vLLM server instructions
    print("\n5. VLLM OPENAI-COMPATIBLE SERVER")
    print("-" * 40)
    vllm_openai_compatible_server()
    
    print("\n" + "=" * 80)
    print("Examples complete! Uncomment code blocks to test with your setup.")
    print("=" * 80)
