#!/usr/bin/env python3
"""
Hugging Face Ecosystem Examples
Demonstrates using transformers, datasets, and inference APIs.
"""

import os
from typing import List, Dict

# =============================================================================
# 1. TRANSFORMERS LIBRARY - BASIC USAGE
# =============================================================================


def example_pipeline_api():
    """
    Use Hugging Face's pipeline API for common NLP tasks.
    Requires: pip install transformers torch
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Pipeline API")
    print("=" * 70)

    try:
        from transformers import pipeline

        # Sentiment Analysis
        print("\n1. Sentiment Analysis")
        print("-" * 40)
        classifier = pipeline("sentiment-analysis")
        result = classifier("I love using Hugging Face models!")
        print(f"Text: 'I love using Hugging Face models!'")
        print(f"Result: {result[0]}")

        # Text Generation
        print("\n2. Text Generation")
        print("-" * 40)
        generator = pipeline("text-generation", model="gpt2")
        result = generator("The future of AI is", max_length=50, num_return_sequences=1)
        print(f"Prompt: 'The future of AI is'")
        print(f"Generated: {result[0]['generated_text']}")

        # Question Answering
        print("\n3. Question Answering")
        print("-" * 40)
        qa = pipeline("question-answering")
        context = (
            "Hugging Face is a company that focuses on natural language processing."
        )
        question = "What does Hugging Face focus on?"
        result = qa(question=question, context=context)
        print(f"Context: {context}")
        print(f"Question: {question}")
        print(f"Answer: {result['answer']} (Score: {result['score']:.2f})")

        # Named Entity Recognition
        print("\n4. Named Entity Recognition")
        print("-" * 40)
        ner = pipeline("ner")
        text = "Elon Musk founded SpaceX in California."
        result = ner(text)
        print(f"Text: {text}")
        print(f"Entities: {result}")

    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Install with: pip install transformers torch")


def example_model_hub_usage():
    """
    Load and use models from Hugging Face Hub.
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Model Hub Usage")
    print("=" * 70)

    try:
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        import torch

        # Load pre-trained model and tokenizer
        model_name = "distilbert-base-uncased-finetuned-sst-2-english"

        print(f"\nLoading model: {model_name}")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(model_name)

        # Prepare input
        texts = [
            "This movie was fantastic!",
            "I hated every minute of it.",
            "The plot was interesting but acting was poor.",
        ]

        print("\nAnalyzing sentiments:")
        print("-" * 40)

        for text in texts:
            inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)

            with torch.no_grad():
                outputs = model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)

            label = "Positive" if predictions[0][1].item() > 0.5 else "Negative"
            confidence = max(predictions[0].tolist())

            print(f"Text: {text}")
            print(f"Sentiment: {label} (Confidence: {confidence:.2%})")
            print()

    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Install with: pip install transformers torch")


# =============================================================================
# 2. DATASETS LIBRARY
# =============================================================================


def example_datasets_usage():
    """
    Load and process datasets using Hugging Face datasets library.
    Requires: pip install datasets
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Datasets Library")
    print("=" * 70)

    try:
        from datasets import load_dataset

        # Load a dataset
        print("\nLoading IMDb dataset (subset)...")
        dataset = load_dataset("imdb", split="train[:100]")

        print(f"\nDataset info:")
        print(f"  Total samples: {len(dataset)}")
        print(f"  Features: {dataset.features}")

        # Access samples
        print("\nSample reviews:")
        print("-" * 40)
        for i in range(3):
            sample = dataset[i]
            sentiment = "Positive" if sample["label"] == 1 else "Negative"
            print(f"\n{i+1}. Sentiment: {sentiment}")
            print(f"   Review: {sample['text'][:100]}...")

        # Process dataset
        print("\n\nProcessing dataset...")
        print("-" * 40)

        def tokenize(example):
            return {"length": len(example["text"].split())}

        dataset_processed = dataset.map(tokenize)

        avg_length = sum(dataset_processed["length"]) / len(dataset_processed)
        print(f"Average review length: {avg_length:.1f} words")

    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Install with: pip install datasets")
    except Exception as e:
        print(f"Error loading dataset: {e}")


# =============================================================================
# 3. INFERENCE API
# =============================================================================


def example_inference_api():
    """
    Use Hugging Face Inference API (no local model needed).
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Inference API")
    print("=" * 70)

    api_token = os.getenv("HF_API_TOKEN", "")

    if not api_token:
        print("\n⚠️  Set HF_API_TOKEN environment variable to use Inference API")
        print("Get token from: https://huggingface.co/settings/tokens")
        print("\nExample usage:")
        print("""
import requests

API_URL = "https://api-inference.huggingface.co/models/gpt2"
headers = {"Authorization": f"Bearer {api_token}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

output = query({"inputs": "The future of AI"})
print(output)
""")
        return

    try:
        import requests

        # Text Generation
        API_URL = "https://api-inference.huggingface.co/models/gpt2"
        headers = {"Authorization": f"Bearer {api_token}"}

        print("\nQuerying GPT-2 via Inference API...")
        payload = {
            "inputs": "The future of artificial intelligence",
            "parameters": {"max_new_tokens": 50, "temperature": 0.7},
        }

        response = requests.post(API_URL, headers=headers, json=payload)
        result = response.json()

        if isinstance(result, list):
            print(f"Generated: {result[0]['generated_text']}")
        else:
            print(f"Response: {result}")

    except Exception as e:
        print(f"Error: {e}")


# =============================================================================
# 4. CUSTOM MODEL TRAINING
# =============================================================================


def example_fine_tuning():
    """
    Example of fine-tuning a model on custom data.
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Fine-Tuning Setup")
    print("=" * 70)

    print("""
Fine-tuning workflow:

1. Prepare your dataset:
   from datasets import load_dataset
   dataset = load_dataset('csv', data_files='your_data.csv')

2. Load pre-trained model and tokenizer:
   from transformers import AutoTokenizer, AutoModelForSequenceClassification
   tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
   model = AutoModelForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)

3. Tokenize dataset:
   def tokenize(batch):
       return tokenizer(batch['text'], padding=True, truncation=True)
   dataset = dataset.map(tokenize, batched=True)

4. Train:
   from transformers import Trainer, TrainingArguments
   training_args = TrainingArguments(
       output_dir='./results',
       num_train_epochs=3,
       per_device_train_batch_size=16,
       evaluation_strategy='epoch'
   )
   
   trainer = Trainer(
       model=model,
       args=training_args,
       train_dataset=dataset['train'],
       eval_dataset=dataset['validation']
   )
   
   trainer.train()

5. Save model:
   model.save_pretrained('./my-finetuned-model')
   tokenizer.save_pretrained('./my-finetuned-model')

For complete tutorial, see:
https://huggingface.co/docs/transformers/training
""")


# =============================================================================
# 5. SPACES SDK
# =============================================================================


def example_spaces_sdk():
    """
    Create a Hugging Face Space demo.
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 6: Gradio App for Spaces")
    print("=" * 70)

    gradio_code = """
import gradio as gr
from transformers import pipeline

# Load model
classifier = pipeline("sentiment-analysis")

# Define prediction function
def analyze_sentiment(text):
    result = classifier(text)[0]
    return {
        "Sentiment": result["label"],
        "Confidence": f"{result['score']:.2%}"
    }

# Create interface
demo = gr.Interface(
    fn=analyze_sentiment,
    inputs=gr.Textbox(placeholder="Enter text here..."),
    outputs="json",
    title="Sentiment Analyzer",
    description="Analyze the sentiment of any text using AI"
)

if __name__ == "__main__":
    demo.launch()
"""

    print("\nGradio App Code:")
    print("-" * 40)
    print(gradio_code)

    print("\n\nTo deploy on Hugging Face Spaces:")
    print("""
1. Create new Space at: https://huggingface.co/spaces
2. Choose Gradio as SDK
3. Upload app.py with the code above
4. Add requirements.txt:
   transformers
   torch
   gradio
   
5. Your app will be live at: https://huggingface.co/spaces/your-username/your-space
""")


# =============================================================================
# 6. MODEL COMPARISON
# =============================================================================


def compare_models():
    """
    Compare different models for the same task.
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 7: Model Comparison")
    print("=" * 70)

    models_comparison = {
        "BERT": {
            "size": "~440MB",
            "speed": "Fast",
            "accuracy": "High",
            "use_case": "General NLP tasks",
        },
        "DistilBERT": {
            "size": "~260MB",
            "speed": "Very Fast",
            "accuracy": "Good",
            "use_case": "Resource-constrained environments",
        },
        "RoBERTa": {
            "size": "~480MB",
            "speed": "Fast",
            "accuracy": "Very High",
            "use_case": "When accuracy is critical",
        },
        "GPT-2": {
            "size": "~1.6GB",
            "speed": "Medium",
            "accuracy": "High",
            "use_case": "Text generation",
        },
        "T5": {
            "size": "~880MB",
            "speed": "Medium",
            "accuracy": "Very High",
            "use_case": "Text-to-text tasks",
        },
    }

    print(f"\n{'Model':<15} {'Size':<12} {'Speed':<12} {'Accuracy':<12} {'Use Case'}")
    print("-" * 70)

    for model, info in models_comparison.items():
        print(
            f"{model:<15} {info['size']:<12} {info['speed']:<12} {info['accuracy']:<12} {info['use_case']}"
        )

    print("\n\nChoose based on your needs:")
    print("- Speed: DistilBERT")
    print("- Accuracy: RoBERTa or T5")
    print("- Balance: BERT")
    print("- Generation: GPT-2")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("HUGGING FACE ECOSYSTEM EXAMPLES")
    print("=" * 80)

    # Run examples
    example_pipeline_api()
    example_model_hub_usage()
    example_datasets_usage()
    example_inference_api()
    example_fine_tuning()
    example_spaces_sdk()
    compare_models()

    print("\n" + "=" * 80)
    print("Examples complete!")
    print("=" * 80)
    print("\nNext steps:")
    print("1. Install dependencies: pip install transformers datasets torch gradio")
    print("2. Get API token: https://huggingface.co/settings/tokens")
    print("3. Explore models: https://huggingface.co/models")
    print("4. Read docs: https://huggingface.co/docs")
