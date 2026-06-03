#!/usr/bin/env python3
"""
Lab 1: Prompt Engineering Patterns
Practice implementing different prompt engineering techniques.

Instructions:
1. Complete each TODO section
2. Test your prompts with an LLM
3. Verify outputs meet the success criteria
"""

from typing import List, Dict

# =============================================================================
# EXERCISE 1: Zero-Shot Classification
# =============================================================================


def exercise_zero_shot_classification():
    """
    Task: Create a zero-shot prompt to classify news articles into categories.

    Categories: Politics, Technology, Sports, Entertainment, Business

    Success Criteria:
    - Prompt clearly defines the task
    - Specifies all available categories
    - Instructs model to output only the category name
    - Works for diverse article topics
    """

    # TODO: Implement this function
    article = """
    The new smartphone features an advanced AI chip that can process 
    neural networks locally on the device, enabling faster image 
    recognition and natural language processing without cloud connectivity.
    """

    prompt = """
    [YOUR PROMPT HERE]
    """

    return prompt


# =============================================================================
# EXERCISE 2: Few-Shot Learning
# =============================================================================


def exercise_few_shot_sentiment():
    """
    Task: Create a few-shot prompt for sentiment analysis with nuanced examples.

    Requirements:
    - Provide at least 3 examples showing different sentiments
    - Include at least one ambiguous/sarcastic example
    - Examples should demonstrate the expected output format

    Success Criteria:
    - Model correctly identifies positive, negative, and neutral sentiments
    - Handles sarcasm appropriately
    - Output includes confidence score
    """

    # TODO: Implement this function
    test_texts = [
        "This is the best product I've ever bought!",
        "It arrived on time, nothing special.",
        "Oh great, another meeting. Just what I needed.",
        "The food was cold and the service was slow.",
    ]

    prompt = """
    [YOUR PROMPT WITH EXAMPLES HERE]
    """

    return prompt


# =============================================================================
# EXERCISE 3: Chain-of-Thought Reasoning
# =============================================================================


def exercise_chain_of_thought():
    """
    Task: Create a chain-of-thought prompt for solving a logic puzzle.

    Puzzle:
    Three friends (Alice, Bob, Carol) have different jobs
    (Engineer, Designer, Manager) and live in different cities
    (NYC, SF, Seattle). Given these clues:
    1. Alice doesn't live in NYC
    2. The Engineer lives in SF
    3. Bob is not the Designer
    4. Carol lives in Seattle

    Who is the Manager and where do they live?

    Success Criteria:
    - Prompt encourages step-by-step reasoning
    - Each deduction is clearly explained
    - Final answer is correct
    - Shows working for verification
    """

    # TODO: Implement this function
    prompt = """
    [YOUR CHAIN-OF-THOUGHT PROMPT HERE]
    """

    return prompt


# =============================================================================
# EXERCISE 4: System Prompt Design
# =============================================================================


def exercise_system_prompt():
    """
    Task: Design a system prompt for a customer support chatbot.

    Requirements:
    - Define the bot's role and personality
    - Set clear constraints (what it can/cannot do)
    - Specify output format
    - Include escalation procedures

    Success Criteria:
    - Bot stays in character
    - Handles inappropriate requests gracefully
    - Provides structured responses
    - Knows when to escalate to human agent
    """

    # TODO: Implement this function
    system_prompt = """
    [YOUR SYSTEM PROMPT HERE]
    """

    return system_prompt


# =============================================================================
# EXERCISE 5: Tool Calling Pattern
# =============================================================================


def exercise_tool_calling():
    """
    Task: Create a tool-calling prompt for a travel assistant.

    Available Tools:
    - flight_search(origin, destination, date)
    - hotel_search(city, check_in, check_out, budget)
    - weather_forecast(city, date)
    - currency_converter(amount, from_currency, to_currency)

    User Request:
    "I'm planning a trip to Paris from New York next month.
    I need a flight, a hotel under $200/night, and want to know
    what the weather will be like. Also, how many euros will $1000 give me?"

    Success Criteria:
    - Prompt clearly defines available tools
    - Model correctly identifies which tools to call
    - Parameters are extracted accurately
    - Multiple tool calls are orchestrated properly
    """

    # TODO: Implement this function
    user_request = """
    I'm planning a trip to Paris from New York next month. 
    I need a flight, a hotel under $200/night, and want to know 
    what the weather will be like. Also, how many euros will $1000 give me?
    """

    prompt = """
    [YOUR TOOL-CALLING PROMPT HERE]
    """

    return prompt


# =============================================================================
# EXERCISE 6: Prompt Evaluation
# =============================================================================


def exercise_prompt_evaluation():
    """
    Task: Create an evaluation prompt to assess generated content.

    Scenario: You've built a prompt to generate product descriptions.
    Create an evaluator prompt that checks:
    - Accuracy (no false claims)
    - Completeness (covers key features)
    - Tone (matches brand voice)
    - Length (100-150 words)
    - Call-to-action included

    Success Criteria:
    - Evaluator provides numerical score
    - Identifies specific issues
    - Suggests concrete improvements
    - Consistent across different inputs
    """

    # TODO: Implement this function
    original_request = "Write a product description for wireless headphones"
    generated_content = """
    [Sample generated content to evaluate]
    These amazing headphones deliver crystal-clear sound with deep bass.
    They feature active noise cancellation, 30-hour battery life, and 
    comfortable ear cushions. Perfect for music lovers and professionals.
    Buy now and experience audio excellence!
    """

    eval_prompt = """
    [YOUR EVALUATION PROMPT HERE]
    """

    return eval_prompt


# =============================================================================
# TESTING HARNESS
# =============================================================================


def test_exercise(exercise_func, exercise_name):
    """Test an exercise function."""
    print(f"\n{'='*60}")
    print(f"Testing: {exercise_name}")
    print("=" * 60)

    try:
        result = exercise_func()
        if "[YOUR" in result or result.strip() == "":
            print("❌ NOT COMPLETED - Replace placeholder with implementation")
            return False
        else:
            print("✅ Completed")
            print("\nGenerated Prompt:")
            print("-" * 40)
            print(result[:500] + "..." if len(result) > 500 else result)
            return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("PROMPT ENGINEERING LAB EXERCISES")
    print("=" * 60)
    print("\nComplete each exercise by replacing the TODO sections.")
    print("Run this script to test your implementations.\n")

    exercises = [
        (exercise_zero_shot_classification, "Exercise 1: Zero-Shot Classification"),
        (exercise_few_shot_sentiment, "Exercise 2: Few-Shot Sentiment"),
        (exercise_chain_of_thought, "Exercise 3: Chain-of-Thought"),
        (exercise_system_prompt, "Exercise 4: System Prompt Design"),
        (exercise_tool_calling, "Exercise 5: Tool Calling"),
        (exercise_prompt_evaluation, "Exercise 6: Prompt Evaluation"),
    ]

    completed = 0
    total = len(exercises)

    for func, name in exercises:
        if test_exercise(func, name):
            completed += 1

    print(f"\n{'='*60}")
    print(f"Progress: {completed}/{total} exercises completed")
    print("=" * 60)

    if completed == total:
        print("\n🎉 All exercises completed successfully!")
    else:
        print(f"\n⚠️  {total - completed} exercises remaining. Keep going!")
