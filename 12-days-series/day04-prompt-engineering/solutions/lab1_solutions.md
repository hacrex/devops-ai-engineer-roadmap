# Day 4: Prompt Engineering - Solutions

## Exercise Solutions and Explanations

---

## Exercise 1: Zero-Shot Classification

### Solution

```python
def exercise_zero_shot_classification():
    article = """
    The new smartphone features an advanced AI chip that can process 
    neural networks locally on the device, enabling faster image 
    recognition and natural language processing without cloud connectivity.
    """
    
    prompt = f"""
Classify the following news article into exactly one of these categories:
- Politics
- Technology  
- Sports
- Entertainment
- Business

Output ONLY the category name, nothing else.

Article:
{article}

Category:
"""
    return prompt
```

### Explanation

**Key Elements:**
1. **Clear task definition**: "Classify the following news article"
2. **Explicit categories**: Lists all available options
3. **Output constraint**: "Output ONLY the category name"
4. **No examples**: Pure zero-shot approach

**Why This Works:**
- LLMs have pre-trained knowledge about topic categories
- Clear constraints prevent verbose outputs
- Simple format enables easy parsing

**Expected Output:**
```
Technology
```

---

## Exercise 2: Few-Shot Sentiment

### Solution

```python
def exercise_few_shot_sentiment():
    prompt = """
Analyze the sentiment of each text and output:
- Sentiment: positive/negative/neutral
- Confidence: 0.0 to 1.0
- Brief reason: one sentence

Example 1:
Text: "This is the best product I've ever bought!"
Sentiment: positive
Confidence: 0.95
Reason: Strong positive language with superlative "best"

Example 2:
Text: "It arrived on time, nothing special."
Sentiment: neutral
Confidence: 0.85
Reason: Factual statement without emotional language

Example 3:
Text: "Oh great, another meeting. Just what I needed."
Sentiment: negative
Confidence: 0.80
Reason: Sarcastic tone indicates frustration

Example 4:
Text: "The food was cold and the service was slow."
Sentiment: negative
Confidence: 0.90
Reason: Explicit complaints about quality and service

Now analyze:
Text: "[INSERT TEXT HERE]"
Sentiment:
Confidence:
Reason:
"""
    return prompt
```

### Explanation

**Key Elements:**
1. **Structured output format**: Consistent fields for each analysis
2. **Diverse examples**: Covers positive, neutral, negative, and sarcastic cases
3. **Confidence scores**: Encourages model to express uncertainty
4. **Reasoning**: Provides transparency for decisions

**Why Few-Shot Works Here:**
- Sentiment can be nuanced and context-dependent
- Examples show how to handle sarcasm
- Output format is learned from examples

---

## Exercise 3: Chain-of-Thought Reasoning

### Solution

```python
def exercise_chain_of_thought():
    prompt = """
Solve this logic puzzle by reasoning through it step by step.

Three friends (Alice, Bob, Carol) have different jobs 
(Engineer, Designer, Manager) and live in different cities 
(NYC, SF, Seattle).

Clues:
1. Alice doesn't live in NYC
2. The Engineer lives in SF
3. Bob is not the Designer
4. Carol lives in Seattle

Question: Who is the Manager and where do they live?

Let's solve this systematically:

Step 1: List what we know directly from the clues
- From clue 4: Carol lives in Seattle
- From clue 1: Alice doesn't live in NYC, so Alice lives in SF or Seattle
  But Carol is in Seattle, so Alice must live in SF
- Therefore: Bob lives in NYC

Step 2: Determine jobs based on locations
- From clue 2: The Engineer lives in SF
- We know Alice lives in SF, so Alice is the Engineer

Step 3: Determine remaining jobs
- From clue 3: Bob is not the Designer
- Bob is not the Designer and not the Engineer (Alice is), so Bob is the Manager
- Therefore: Carol is the Designer

Step 4: Answer the question
- Bob is the Manager
- Bob lives in NYC

Final Answer: Bob is the Manager and he lives in NYC.
"""
    return prompt
```

### Explanation

**Chain-of-Thought Benefits:**
1. **Explicit reasoning**: Shows each deduction clearly
2. **Verifiable steps**: Easy to check logic at each stage
3. **Error detection**: Mistakes are easier to spot
4. **Teaching value**: Helps learners understand the approach

**Why It Works:**
- Breaks complex problems into manageable steps
- Forces systematic thinking
- Reduces hallucination by grounding each claim

---

## Exercise 4: System Prompt Design

### Solution

```python
def exercise_system_prompt():
    system_prompt = """
You are SupportBot, a friendly and professional customer support assistant 
for TechCorp, a consumer electronics company.

ROLE & PERSONALITY:
- Be warm, empathetic, and solution-oriented
- Use clear, jargon-free language
- Show understanding of customer frustrations
- Maintain professionalism even with difficult customers

CONSTRAINTS - What You CAN Do:
✓ Answer product questions using provided knowledge base
✓ Help with order status (ask for order number)
✓ Guide through basic troubleshooting steps
✓ Process returns/exchanges within policy
✓ Escalate complex technical issues to human agents

CONSTRAINTS - What You CANNOT Do:
✗ Make promises about delivery dates
✗ Approve refunds outside of policy
✗ Access customer payment information
✗ Provide technical support for third-party products
✗ Give medical, legal, or financial advice

OUTPUT FORMAT:
Structure your responses as:
1. Acknowledge the customer's concern
2. Provide relevant information or solution
3. Ask if there's anything else you can help with
4. If escalating, explain next steps clearly

ESCALATION PROCEDURE:
When you need to escalate to a human agent:
1. Acknowledge the limitation: "I understand this requires specialized assistance"
2. Explain what will happen: "I'm connecting you with a specialist who..."
3. Set expectations: "They'll reach out within 24 hours via email"
4. Confirm contact info if needed

HANDLING INAPPROPRIATE REQUESTS:
If a request violates policies or is inappropriate:
- Politely decline: "I'm not able to assist with that"
- Briefly explain why (if appropriate)
- Offer alternative help: "However, I can help you with..."

EXAMPLE INTERACTION:
Customer: "My laptop won't turn on!"
SupportBot: "I understand how frustrating that can be, especially when 
you need to get work done. Let's try some basic troubleshooting steps:

1. Check if the power cable is securely connected
2. Try a different power outlet
3. Hold the power button for 10 seconds, then try turning it on again

Did any of these steps work? If not, I can connect you with our technical 
support team for more advanced troubleshooting."

Remember: Your goal is to resolve issues efficiently while making customers 
feel heard and valued.
"""
    return system_prompt
```

### Explanation

**Comprehensive System Prompt Elements:**

1. **Role Definition**: Clear identity and context
2. **Personality Guidelines**: Tone and communication style
3. **Capability Boundaries**: Explicit can/cannot lists
4. **Output Structure**: Consistent response format
5. **Edge Case Handling**: Escalation and refusal patterns
6. **Examples**: Concrete demonstrations of expected behavior

**Best Practices Applied:**
- Uses visual markers (✓/✗) for clarity
- Provides specific scenarios
- Includes example interaction
- Balances friendliness with professionalism

---

## Exercise 5: Tool Calling

### Solution

```python
def exercise_tool_calling():
    prompt = """
You are a travel assistant with access to these tools:

AVAILABLE TOOLS:

1. flight_search
   Description: Search for flights between cities
   Parameters:
     - origin: string (airport code or city name)
     - destination: string (airport code or city name)
     - date: string (YYYY-MM-DD format)
   
2. hotel_search
   Description: Find hotels in a city
   Parameters:
     - city: string
     - check_in: string (YYYY-MM-DD)
     - check_out: string (YYYY-MM-DD)
     - budget: number (max price per night in USD)

3. weather_forecast
   Description: Get weather forecast for a city
   Parameters:
     - city: string
     - date: string (YYYY-MM-DD)

4. currency_converter
   Description: Convert between currencies
   Parameters:
     - amount: number
     - from_currency: string (3-letter code like USD)
     - to_currency: string (3-letter code like EUR)

INSTRUCTIONS:
- To use a tool, respond with JSON in this exact format:
  {"tool": "tool_name", "parameters": {param1: value1, param2: value2}}
- For multiple tools, output multiple JSON objects separated by newlines
- Extract all necessary parameters from the user's request
- If information is missing (like specific dates), use reasonable defaults
  or ask for clarification

USER REQUEST:
"I'm planning a trip to Paris from New York next month. 
I need a flight, a hotel under $200/night, and want to know 
what the weather will be like. Also, how many euros will $1000 give me?"

RESPONSE:
"""
    
    # Expected model output:
    expected_tools = [
        '{"tool": "flight_search", "parameters": {"origin": "New York", "destination": "Paris", "date": "2024-02-15"}}',
        '{"tool": "hotel_search", "parameters": {"city": "Paris", "check_in": "2024-02-15", "check_out": "2024-02-22", "budget": 200}}',
        '{"tool": "weather_forecast", "parameters": {"city": "Paris", "date": "2024-02-15"}}',
        '{"tool": "currency_converter", "parameters": {"amount": 1000, "from_currency": "USD", "to_currency": "EUR"}}'
    ]
    
    return prompt
```

### Explanation

**Tool Calling Best Practices:**

1. **Clear Tool Definitions**: Each tool has name, description, and schema
2. **Parameter Specifications**: Types and formats are explicit
3. **Output Format**: JSON structure is precisely defined
4. **Multiple Tools**: Supports batch tool invocation
5. **Handling Ambiguity**: Guidance for missing information

**Why This Pattern Works:**
- Separates intent (natural language) from execution (structured calls)
- Enables reliable parameter extraction
- Supports complex multi-step workflows
- Easy to parse and execute programmatically

---

## Exercise 6: Prompt Evaluation

### Solution

```python
def exercise_prompt_evaluation():
    eval_prompt = """
You are an expert evaluator of AI-generated content. Evaluate the following 
product description against these criteria:

EVALUATION CRITERIA:

1. ACCURACY (25 points)
   - No false or misleading claims
   - Features described match typical product specifications
   - No exaggerated performance claims

2. COMPLETENESS (25 points)
   - Covers key features (sound quality, battery, comfort, connectivity)
   - Mentions important specifications
   - Addresses common buyer concerns

3. TONE (20 points)
   - Matches premium brand voice (professional yet approachable)
   - Enthusiastic without being hyperbolic
   - Builds trust with readers

4. LENGTH (15 points)
   - Between 100-150 words
   - Concise but informative
   - No unnecessary filler

5. CALL-TO-ACTION (15 points)
   - Includes clear CTA
   - Creates sense of urgency or value
   - Guides reader to next step

INPUT:
Original Request: "Write a product description for wireless headphones"

Generated Content:
"These amazing headphones deliver crystal-clear sound with deep bass.
They feature active noise cancellation, 30-hour battery life, and 
comfortable ear cushions. Perfect for music lovers and professionals.
Buy now and experience audio excellence!"

EVALUATION OUTPUT FORMAT:
Provide your evaluation as valid JSON:

{
  "overall_score": <number 0-100>,
  "breakdown": {
    "accuracy": {"score": <0-25>, "comments": "<specific feedback>"},
    "completeness": {"score": <0-25>, "comments": "<specific feedback>"},
    "tone": {"score": <0-20>, "comments": "<specific feedback>"},
    "length": {"score": <0-15>, "comments": "<word count and feedback>"},
    "call_to_action": {"score": <0-15>, "comments": "<specific feedback>"}
  },
  "issues_found": ["<list each specific issue>"],
  "improvements": ["<concrete suggestions for each issue>"],
  "revised_version": "<your improved version of the description>"
}
"""
    return eval_prompt
```

### Explanation

**Evaluation Prompt Design:**

1. **Weighted Criteria**: Different aspects have appropriate importance
2. **Clear Rubrics**: Each criterion has specific scoring guidelines
3. **Structured Output**: JSON format enables automated processing
4. **Actionable Feedback**: Requires specific issues and improvements
5. **Model Revision**: Asks evaluator to provide corrected version

**Benefits of This Approach:**
- Quantitative scoring enables tracking over time
- Qualitative feedback provides actionable insights
- Revised version serves as training data
- Consistent format allows comparison across evaluations

---

## Key Takeaways

### Prompt Engineering Principles

1. **Clarity Over Cleverness**: Simple, direct instructions work best
2. **Examples Are Powerful**: Few-shot learning dramatically improves results
3. **Structure Matters**: Well-formatted prompts get well-formatted outputs
4. **Constraints Enable Creativity**: Boundaries focus the model's capabilities
5. **Iteration Is Essential**: Test, evaluate, and refine continuously

### Common Patterns

| Pattern | When to Use | Key Benefit |
|---------|-------------|-------------|
| Zero-Shot | Simple, well-defined tasks | Fast, no examples needed |
| Few-Shot | Nuanced tasks, specific formats | Teaches by example |
| Chain-of-Thought | Complex reasoning, math, logic | Improves accuracy |
| System Prompts | Role-based interactions | Consistent behavior |
| Tool Calling | External API integration | Extends capabilities |
| Evaluation | Quality assurance | Enables iteration |

### Testing Your Prompts

Always test prompts with:
- ✅ Typical inputs
- ✅ Edge cases
- ✅ Adversarial examples
- ✅ Different phrasings of same request
- ✅ Various output validation checks

---

*Day 4 Solutions - Prompt Engineering Mastery*
