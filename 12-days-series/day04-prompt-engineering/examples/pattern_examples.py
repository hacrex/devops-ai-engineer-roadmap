#!/usr/bin/env python3
"""
Prompt Engineering Pattern Examples
Demonstrates zero-shot, few-shot, chain-of-thought, and tool calling patterns.
"""

from typing import List, Dict, Any

# =============================================================================
# 1. ZERO-SHOT PROMPTING
# =============================================================================


def zero_shot_sentiment(text: str) -> str:
    """Classify sentiment without examples."""
    prompt = f"""
Classify the sentiment of this text as positive, negative, or neutral.
Do not explain your reasoning, just output the classification.

Text: "{text}"
Sentiment:
"""
    return prompt


def zero_shot_classification(task: str, data: str) -> str:
    """Generic zero-shot classifier."""
    prompt = f"""
Perform the following task on the provided data.

Task: {task}
Data: {data}

Result:
"""
    return prompt


# =============================================================================
# 2. FEW-SHOT PROMPTING
# =============================================================================


def few_shot_entity_extraction(text: str) -> str:
    """Extract entities using few-shot examples."""
    prompt = f"""
Extract entities from text. Identify PERSON, ORGANIZATION, LOCATION, DATE, and PRODUCT.

Example 1:
Text: "Apple released new iPhones in Cupertino"
Entities: {{"ORG": ["Apple"], "PRODUCT": ["iPhones"], "LOCATION": ["Cupertino"]}}

Example 2:
Text: "Elon Musk founded SpaceX in 2002"
Entities: {{"PERSON": ["Elon Musk"], "ORG": ["SpaceX"], "DATE": ["2002"]}}

Example 3:
Text: "Microsoft launched Windows 11 in Seattle last year"
Entities: {{"ORG": ["Microsoft"], "PRODUCT": ["Windows 11"], "LOCATION": ["Seattle"], "DATE": ["last year"]}}

Now extract from:
Text: "{text}"
Entities:
"""
    return prompt


def few_shot_text_transformation(input_text: str, transformation_type: str) -> str:
    """Transform text based on examples."""
    examples = {
        "summarize": [
            ("The quick brown fox jumps over the lazy dog.", "Fox jumps over dog."),
            (
                "Machine learning is a subset of AI that enables systems to learn from data.",
                "ML learns from data.",
            ),
        ],
        "formalize": [
            ("hey whats up", "Hello, how are you?"),
            ("gonna be late", "I will be arriving late."),
        ],
    }

    prompt = f"""
Transform the text according to the pattern shown in examples.

"""
    if transformation_type in examples:
        for i, (inp, out) in enumerate(examples[transformation_type], 1):
            prompt += f'Example {i}:\nInput: "{inp}"\nOutput: "{out}"\n\n'

    prompt += f"""Now transform:
Input: "{input_text}"
Output:
"""
    return prompt


# =============================================================================
# 3. CHAIN-OF-THOUGHT PROMPTING
# =============================================================================


def cot_math_problem(problem: str) -> str:
    """Solve math problems with step-by-step reasoning."""
    prompt = f"""
Solve the following problem. Show your reasoning step by step before giving the final answer.

Problem: {problem}

Let's think step by step:
"""
    return prompt


def cot_logical_reasoning(scenario: str, question: str) -> str:
    """Analyze scenarios with logical reasoning."""
    prompt = f"""
Analyze the scenario and answer the question. Break down your reasoning into clear steps.

Scenario: {scenario}

Question: {question}

Reasoning steps:
1. First, let's identify the key facts:
2. Next, let's analyze the relationships:
3. Then, we can deduce:
4. Therefore:

Answer:
"""
    return prompt


def cot_debugging(code: str, error: str) -> str:
    """Debug code systematically."""
    prompt = f"""
Debug the following code that produces an error. Analyze it step by step.

Code:
```python
{code}
```

Error: {error}

Debugging process:
1. First, let's understand what the code is trying to do:
2. Let's trace through the execution:
3. The error occurs because:
4. To fix this, we should:

Corrected code:
"""
    return prompt


# =============================================================================
# 4. SYSTEM PROMPTS & CONTEXT MANAGEMENT
# =============================================================================


def create_system_prompt(role: str, constraints: List[str], output_format: str) -> str:
    """Create a structured system prompt."""
    constraints_str = "\n".join(f"- {c}" for c in constraints)

    prompt = f"""You are a {role}. Follow these constraints strictly:

{constraints_str}

Always format your output as: {output_format}

Remember:
- Stay in character at all times
- If you don't know something, say so
- Never break the constraints above
"""
    return prompt


def build_context_window(
    context_items: List[Dict[str, str]], max_tokens: int = 4000
) -> str:
    """Build a context window from multiple items."""
    context = "Relevant Context:\n\n"
    token_count = len(context)

    for i, item in enumerate(context_items, 1):
        item_text = (
            f"[{i}] {item.get('source', 'Unknown')}: {item.get('content', '')}\n\n"
        )
        if token_count + len(item_text) > max_tokens:
            break
        context += item_text
        token_count += len(item_text)

    context += "\nBased on the context above, answer the user's question.\n"
    return context


# =============================================================================
# 5. TOOL CALLING PATTERNS
# =============================================================================

TOOL_DEFINITIONS = {
    "calculator": {
        "name": "calculator",
        "description": "Perform mathematical calculations",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Math expression to evaluate",
                }
            },
            "required": ["expression"],
        },
    },
    "search": {
        "name": "web_search",
        "description": "Search the web for current information",
        "parameters": {
            "type": "object",
            "properties": {"query": {"type": "string", "description": "Search query"}},
            "required": ["query"],
        },
    },
    "weather": {
        "name": "get_weather",
        "description": "Get weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "City name"},
                "date": {"type": "string", "description": "Date (YYYY-MM-DD)"},
            },
            "required": ["location"],
        },
    },
}


def create_tool_calling_prompt(question: str, available_tools: List[str]) -> str:
    """Create a prompt that enables tool calling."""
    tools_json = ",\n  ".join(
        str(TOOL_DEFINITIONS[tool])
        for tool in available_tools
        if tool in TOOL_DEFINITIONS
    )

    prompt = f"""You are a helpful assistant with access to the following tools:

Tools:
[
  {tools_json}
]

To use a tool, respond with a JSON object in this format:
{{
  "tool": "<tool_name>",
  "parameters": {{<key-value pairs>}}
}}

If you don't need a tool, just answer normally.

User question: {question}

Response:
"""
    return prompt


def parse_tool_response(response: str) -> Dict[str, Any]:
    """Parse a tool call from model response."""
    import json
    import re

    # Try to extract JSON from response
    json_match = re.search(r"\{[^}]*\}", response, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass
    return {"tool": None, "parameters": {}}


# =============================================================================
# 6. EVALUATION PROMPTS
# =============================================================================


def create_evaluation_prompt(original: str, generated: str, criteria: List[str]) -> str:
    """Evaluate generated content against criteria."""
    criteria_str = "\n".join(f"- {c}" for c in criteria)

    prompt = f"""
Evaluate the generated content against the following criteria:

{criteria_str}

Original Request:
{original}

Generated Content:
{generated}

Provide your evaluation as JSON:
{{
  "score": <1-10>,
  "feedback": "<detailed feedback>",
  "meets_criteria": {{<criterion>: true/false for each>}},
  "suggestions": ["<improvement suggestions>"]
}}
"""
    return prompt


# =============================================================================
# MAIN DEMONSTRATION
# =============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("PROMPT ENGINEERING PATTERN EXAMPLES")
    print("=" * 80)

    # Zero-shot example
    print("\n1. ZERO-SHOT PROMPTING")
    print("-" * 40)
    prompt = zero_shot_sentiment("I absolutely love this product!")
    print(prompt)

    # Few-shot example
    print("\n2. FEW-SHOT PROMPTING")
    print("-" * 40)
    prompt = few_shot_entity_extraction("Tesla opened a new factory in Berlin in 2023")
    print(prompt)

    # Chain-of-thought example
    print("\n3. CHAIN-OF-THOUGHT PROMPTING")
    print("-" * 40)
    prompt = cot_math_problem(
        "If a train travels at 80 mph for 2.5 hours, then stops for 30 minutes, how far has it traveled?"
    )
    print(prompt)

    # System prompt example
    print("\n4. SYSTEM PROMPT")
    print("-" * 40)
    prompt = create_system_prompt(
        role="technical writer",
        constraints=[
            "Use clear, concise language",
            "Include code examples where relevant",
            "Avoid jargon unless defined",
        ],
        output_format="Markdown with headers and bullet points",
    )
    print(prompt)

    # Tool calling example
    print("\n5. TOOL CALLING PROMPT")
    print("-" * 40)
    prompt = create_tool_calling_prompt(
        "What's the weather in Tokyo today and what's 15% of 240?",
        ["weather", "calculator"],
    )
    print(prompt)

    print("\n" + "=" * 80)
    print("All examples generated successfully!")
    print("=" * 80)
