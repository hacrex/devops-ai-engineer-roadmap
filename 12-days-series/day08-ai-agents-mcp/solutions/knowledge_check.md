# 📝 Day 08: Knowledge Check Solutions

## Question 1: What are the three core components of an AI agent?

**Correct Answer:** Planning, Memory, Action

**Explanation:**
AI agents consist of three fundamental components:

1. **Planning Module**: Breaks down complex goals into actionable steps, determines the sequence of actions needed to achieve objectives.

2. **Memory Store**: Maintains context across interactions, stores experiences, learned patterns, and conversation history for informed decision-making.

3. **Action Executor**: Interfaces with external tools and services via MCP to execute planned actions and interact with the environment.

These components work together in a feedback loop where the agent perceives its environment, reasons about the situation, acts to achieve goals, and learns from outcomes.

---

## Question 2: What does MCP standardize?

**Correct Answer:** Tool calling interfaces

**Explanation:**
The Model Context Protocol (MCP) standardizes:

- **Tool Discovery**: How agents find and enumerate available tools
- **Message Structure**: Uniform format for tool calls and responses
- **Context Management**: Consistent handling of session state
- **Error Handling**: Standardized error reporting and recovery

MCP does NOT standardize model training procedures or hardware specifications - those are separate concerns handled by other protocols and frameworks.

---

## Question 3: Which pattern involves self-reflection?

**Correct Answer:** Reflexion

**Explanation:**

**Reflexion Pattern:**
```
Attempt → Self-Reflection → Improved Attempt → ...
```
This pattern explicitly includes a self-reflection step where the agent evaluates its previous attempts and uses those insights to improve future actions.

**Other Patterns:**

- **ReAct (Reason + Act)**: `Thought → Action → Observation → Thought → ...`
  - Focuses on interleaving reasoning with action
  - Does not explicitly include reflection on past performance

- **Plan-and-Solve**: `Goal → Plan → Execute Steps → Synthesize → Result`
  - Emphasizes upfront planning before execution
  - More linear than iterative

---

## Question 4: How do agents maintain context across interactions?

**Correct Answer:** Through memory stores

**Explanation:**
Agents maintain context using various memory mechanisms:

1. **Short-term Memory**: Stores the current conversation/session context
   - Recent messages and tool calls
   - Current task state and progress

2. **Long-term Memory**: Persists information across sessions
   - User preferences and history
   - Learned patterns and strategies
   - Vector embeddings for semantic search

3. **Working Memory**: Temporary storage for active reasoning
   - Intermediate computation results
   - Current plan execution state

**Implementation Example:**
```python
class AgentMemory:
    def __init__(self):
        self.short_term = []  # Recent interactions
        self.long_term = {}   # Persistent knowledge
        self.context_id = generate_session_id()
    
    def add_interaction(self, message_type, content):
        self.short_term.append({
            "type": message_type,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_context(self, window=10):
        return self.short_term[-window:]
```

Agents do NOT maintain context by retraining on each interaction (too slow and expensive) or using static configurations (inflexible).

---

## Additional Practice

### Exercise 1: Identify Agent Components

For each scenario, identify which component (Planning, Memory, or Action) is primarily involved:

1. An agent remembers your preference for metric units
   - **Answer:** Memory

2. An agent breaks "research climate change" into search, summarize, and cite steps
   - **Answer:** Planning

3. An agent calls a weather API to get current temperature
   - **Answer:** Action

### Exercise 2: MCP Message Validation

Which of these is a valid MCP tool call message?

A) `{"tool": "search", "query": "AI news"}`
B) `{"type": "tool_call", "tool_name": "search_web", "parameters": {"query": "AI news"}}`
C) `{"action": "call_tool", "name": "search", "args": "AI news"}`

- **Answer:** B - Follows the standard MCP structure with type, tool_name, and parameters

### Exercise 3: Pattern Recognition

Match the pattern to its description:

1. ReAct          a) Iterative improvement through self-evaluation
2. Plan-and-Solve b) Interleaved reasoning and action
3. Reflexion      c) Upfront planning followed by execution

- **Answers:** 1-b, 2-c, 3-a

---

## Scoring Guide

- **4/4 Correct**: Excellent! You have a solid understanding of AI agents and MCP.
- **3/4 Correct**: Good job! Review the explanations for any missed questions.
- **2/4 Correct**: Fair understanding. Re-read the relevant sections in the README.
- **0-1/4 Correct**: Review the core concepts section and examples before proceeding.

---

**Next Steps:** Continue with the lab exercises to reinforce your understanding!
