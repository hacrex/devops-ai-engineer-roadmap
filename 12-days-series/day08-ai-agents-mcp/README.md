# 🤖 Day 08: AI Agents & MCP (Model Context Protocol)

## 📋 Overview

Welcome to Day 8! Today we dive into AI Agents and the Model Context Protocol (MCP), which enables AI models to interact with external tools, data sources, and services in a standardized way.

### What You'll Learn

- **AI Agents**: Autonomous systems that can perceive, reason, and act
- **MCP Fundamentals**: Standardized protocol for model-context interactions
- **Tool Integration**: Connecting LLMs to external APIs and databases
- **Agent Architectures**: Planning, memory, and action execution
- **Practical Implementation**: Building your first MCP-enabled agent

### Learning Objectives

By the end of this module, you will:
- Understand the architecture of AI agents
- Implement MCP for standardized tool calling
- Build agents with memory and planning capabilities
- Integrate multiple tools into a cohesive agent system
- Deploy agents in production environments

**Estimated Time**: 4-5 hours  
**Difficulty**: Intermediate  
**Prerequisites**: Python basics, understanding of LLMs (Days 4-5)

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    AI Agent System                       │
├─────────────────────────────────────────────────────────┤
│  ┌──────────────┐    ┌──────────────┐    ┌───────────┐ │
│  │   Planning   │───▶│   Memory     │───▶│  Action   │ │
│  │   Module     │    │   Store      │    │  Executor │ │
│  └──────────────┘    └──────────────┘    └───────────┘ │
│         │                   │                  │        │
│         ▼                   ▼                  ▼        │
│  ┌──────────────────────────────────────────────────┐   │
│  │          Model Context Protocol (MCP)            │   │
│  └──────────────────────────────────────────────────┘   │
│         │                   │                  │        │
│         ▼                   ▼                  ▼        │
│  ┌──────────────┐    ┌──────────────┐    ┌───────────┐ │
│  │   Search     │    │  Database    │    │    API    │ │
│  │   Tools      │    │   Tools      │    │   Tools   │ │
│  └──────────────┘    └──────────────┘    └───────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## 📚 Core Concepts

### 1. What are AI Agents?

AI Agents are autonomous systems that can:
- **Perceive**: Gather information from environment
- **Reason**: Process information and make decisions
- **Act**: Execute actions to achieve goals
- **Learn**: Improve performance over time

#### Key Components:

1. **Planning Module**: Breaks down complex tasks into steps
2. **Memory**: Stores context, experiences, and learned patterns
3. **Action Executor**: Interfaces with external tools via MCP
4. **Feedback Loop**: Evaluates outcomes and adjusts strategy

### 2. Model Context Protocol (MCP)

MCP is a standardized protocol that enables:
- **Tool Discovery**: Agents can discover available tools dynamically
- **Standardized Calling**: Uniform interface for tool invocation
- **Context Management**: Maintains state across interactions
- **Error Handling**: Graceful degradation and retry mechanisms

#### MCP Message Structure:

```json
{
  "type": "tool_call",
  "tool_name": "search_web",
  "parameters": {
    "query": "latest AI developments",
    "num_results": 5
  },
  "context_id": "session_123",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### 3. Agent Architectures

#### ReAct Pattern (Reason + Act):
```
Thought → Action → Observation → Thought → ... → Answer
```

#### Plan-and-Solve:
```
Goal → Plan → Execute Steps → Synthesize → Result
```

#### Reflexion:
```
Attempt → Self-Reflection → Improved Attempt → ...
```

---

## 🔧 Hands-On Examples

### Example 1: Basic Agent with Tool Calling

Let's create a simple agent that can perform web searches and calculations.

**File**: `examples/basic_agent.py`

```python
import json
from typing import Dict, Any, List
from datetime import datetime

class MCPTool:
    """Base class for MCP-compatible tools"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        raise NotImplementedError
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self._get_param_schema()
        }
    
    def _get_param_schema(self) -> Dict[str, Any]:
        return {}


class SearchTool(MCPTool):
    """Web search tool"""
    
    def __init__(self):
        super().__init__(
            name="search_web",
            description="Search the web for information"
        )
    
    def _get_param_schema(self) -> Dict[str, Any]:
        return {
            "query": {"type": "string", "description": "Search query"},
            "num_results": {"type": "integer", "description": "Number of results", "default": 5}
        }
    
    def execute(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        # Simulated search (replace with actual API call)
        results = [
            f"Result {i+1} for '{query}'" for i in range(num_results)
        ]
        return {
            "success": True,
            "results": results,
            "timestamp": datetime.now().isoformat()
        }


class CalculatorTool(MCPTool):
    """Calculator tool for mathematical operations"""
    
    def __init__(self):
        super().__init__(
            name="calculate",
            description="Perform mathematical calculations"
        )
    
    def _get_param_schema(self) -> Dict[str, Any]:
        return {
            "expression": {"type": "string", "description": "Mathematical expression"}
        }
    
    def execute(self, expression: str) -> Dict[str, Any]:
        try:
            # Safe evaluation (in production, use proper parser)
            result = eval(expression, {"__builtins__": {}}, {})
            return {
                "success": True,
                "result": result,
                "expression": expression
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


class SimpleAgent:
    """Basic AI Agent with MCP support"""
    
    def __init__(self):
        self.tools: Dict[str, MCPTool] = {}
        self.memory: List[Dict[str, Any]] = []
        self.context_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def register_tool(self, tool: MCPTool):
        """Register a tool with the agent"""
        self.tools[tool.name] = tool
        print(f"✅ Registered tool: {tool.name}")
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """List all available tools"""
        return [tool.get_schema() for tool in self.tools.values()]
    
    def execute_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """Execute a tool via MCP"""
        if tool_name not in self.tools:
            return {
                "success": False,
                "error": f"Tool '{tool_name}' not found"
            }
        
        # Log the tool call
        call_record = {
            "type": "tool_call",
            "tool_name": tool_name,
            "parameters": kwargs,
            "context_id": self.context_id,
            "timestamp": datetime.now().isoformat()
        }
        self.memory.append(call_record)
        
        # Execute the tool
        result = self.tools[tool_name].execute(**kwargs)
        
        # Log the result
        result_record = {
            "type": "tool_result",
            "tool_name": tool_name,
            "result": result,
            "context_id": self.context_id,
            "timestamp": datetime.now().isoformat()
        }
        self.memory.append(result_record)
        
        return result
    
    def chat(self, user_input: str) -> str:
        """Process user input and respond"""
        # Simple keyword-based routing (replace with LLM in production)
        self.memory.append({
            "type": "user_message",
            "content": user_input,
            "timestamp": datetime.now().isoformat()
        })
        
        if "search" in user_input.lower():
            query = user_input.split("search")[-1].strip()
            result = self.execute_tool("search_web", query=query)
            return f"Search results:\n" + "\n".join(result.get("results", []))
        
        elif any(op in user_input for op in ["+", "-", "*", "/"]):
            result = self.execute_tool("calculate", expression=user_input)
            if result["success"]:
                return f"Result: {result['result']}"
            else:
                return f"Calculation error: {result['error']}"
        
        else:
            return "I can help with searches or calculations. Try asking me to 'search for X' or give me a math expression."
    
    def get_context(self) -> List[Dict[str, Any]]:
        """Retrieve conversation context"""
        return self.memory


# Demo usage
if __name__ == "__main__":
    print("🤖 Initializing AI Agent with MCP...\n")
    
    agent = SimpleAgent()
    
    # Register tools
    agent.register_tool(SearchTool())
    agent.register_tool(CalculatorTool())
    
    print("\n📋 Available tools:")
    for tool in agent.list_tools():
        print(f"  - {tool['name']}: {tool['description']}")
    
    print("\n💬 Chat with the agent (type 'quit' to exit):\n")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
        
        response = agent.chat(user_input)
        print(f"Agent: {response}\n")
    
    print(f"\n📊 Session context saved: {len(agent.memory)} interactions")
```

**Run the example**:
```bash
cd day08-ai-agents-mcp/examples
python basic_agent.py
```

### Example 2: Multi-Step Planning Agent

This agent can break down complex tasks into multiple steps.

**File**: `examples/planning_agent.py`

```python
import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class Task:
    id: str
    description: str
    tool_name: str
    parameters: Dict[str, Any]
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[Dict[str, Any]] = None

@dataclass
class Plan:
    goal: str
    tasks: List[Task]
    current_step: int = 0

class PlanningAgent:
    """Agent with planning capabilities"""
    
    def __init__(self):
        self.plans: List[Plan] = []
        self.current_plan: Optional[Plan] = None
    
    def create_plan(self, goal: str, tasks: List[Dict[str, Any]]) -> Plan:
        """Create a multi-step plan"""
        task_objects = [
            Task(
                id=f"task_{i}",
                description=t.get("description", ""),
                tool_name=t["tool_name"],
                parameters=t.get("parameters", {})
            )
            for i, t in enumerate(tasks)
        ]
        
        plan = Plan(goal=goal, tasks=task_objects)
        self.plans.append(plan)
        self.current_plan = plan
        
        return plan
    
    def execute_next_step(self) -> Optional[Dict[str, Any]]:
        """Execute the next step in the current plan"""
        if not self.current_plan:
            return None
        
        plan = self.current_plan
        if plan.current_step >= len(plan.tasks):
            return {"status": "plan_completed", "goal": plan.goal}
        
        task = plan.tasks[plan.current_step]
        task.status = TaskStatus.IN_PROGRESS
        
        print(f"🔄 Executing: {task.description}")
        
        # Simulate tool execution (integrate with actual tools)
        result = self._execute_tool(task.tool_name, task.parameters)
        
        task.result = result
        task.status = TaskStatus.COMPLETED if result.get("success") else TaskStatus.FAILED
        
        plan.current_step += 1
        
        return {
            "task_id": task.id,
            "description": task.description,
            "status": task.status.value,
            "result": result
        }
    
    def _execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool (placeholder for actual implementation)"""
        # In production, this would call actual tools via MCP
        return {
            "success": True,
            "data": f"Executed {tool_name} with {parameters}"
        }
    
    def get_plan_status(self) -> Dict[str, Any]:
        """Get current plan status"""
        if not self.current_plan:
            return {"status": "no_active_plan"}
        
        completed = sum(1 for t in self.current_plan.tasks if t.status == TaskStatus.COMPLETED)
        total = len(self.current_plan.tasks)
        
        return {
            "goal": self.current_plan.goal,
            "progress": f"{completed}/{total}",
            "current_step": self.current_plan.current_step,
            "tasks": [asdict(t) for t in self.current_plan.tasks]
        }


# Demo usage
if __name__ == "__main__":
    print("🎯 Planning Agent Demo\n")
    
    agent = PlanningAgent()
    
    # Create a complex plan
    plan = agent.create_plan(
        goal="Research and summarize AI trends",
        tasks=[
            {
                "description": "Search for latest AI papers",
                "tool_name": "search_arxiv",
                "parameters": {"query": "transformer architectures", "limit": 10}
            },
            {
                "description": "Extract key findings",
                "tool_name": "extract_summary",
                "parameters": {"source": "search_results"}
            },
            {
                "description": "Generate report",
                "tool_name": "generate_report",
                "parameters": {"format": "markdown"}
            }
        ]
    )
    
    print(f"📋 Plan created: {plan.goal}")
    print(f"   Total tasks: {len(plan.tasks)}\n")
    
    # Execute plan step by step
    while True:
        result = agent.execute_next_step()
        if result["status"] == "plan_completed":
            print(f"\n✅ Plan completed: {result['goal']}")
            break
        print(f"   Status: {result['status']}\n")
    
    # Show final status
    print("\n📊 Final Plan Status:")
    status = agent.get_plan_status()
    print(f"Progress: {status['progress']}")
```

---

## 🧪 Lab Exercises

### Lab 1: Build a Weather Agent ⭐

**Objective**: Create an agent that can fetch weather information using MCP.

**Requirements**:
1. Create a `WeatherTool` class that simulates weather API calls
2. Implement temperature conversion (Celsius ↔ Fahrenheit)
3. Add location-based queries
4. Test with multiple cities

**Starter Code**: See `labs/lab1_weather_agent/`

**Success Criteria**:
- [ ] Agent can retrieve weather for any city
- [ ] Supports temperature unit conversion
- [ ] Handles errors gracefully
- [ ] Logs all interactions via MCP

### Lab 2: Multi-Tool Research Assistant ⭐⭐

**Objective**: Build a research assistant that combines search, summarization, and citation tools.

**Requirements**:
1. Implement at least 3 different tools:
   - Web search
   - Text summarization
   - Citation formatter
2. Create a planning system for multi-step research tasks
3. Maintain conversation history
4. Export research reports

**Starter Code**: See `labs/lab2_research_assistant/`

**Success Criteria**:
- [ ] All three tools work correctly
- [ ] Agent can execute multi-step plans
- [ ] Generates formatted research reports
- [ ] Proper MCP message logging

### Lab 3: Autonomous Task Executor ⭐⭐⭐

**Objective**: Create an agent that can autonomously complete complex workflows.

**Requirements**:
1. Implement ReAct pattern (Reason + Act)
2. Add self-reflection and error recovery
3. Support dynamic tool discovery
4. Handle concurrent task execution

**Starter Code**: See `labs/lab3_autonomous_agent/`

**Success Criteria**:
- [ ] Agent demonstrates reasoning before actions
- [ ] Recovers from failed tool calls
- [ ] Discovers and uses new tools dynamically
- [ ] Manages multiple tasks concurrently

---

## 📝 Knowledge Check

1. **What are the three core components of an AI agent?**
   - [ ] Planning, Memory, Action
   - [ ] Input, Processing, Output
   - [ ] Data, Model, Inference

2. **What does MCP standardize?**
   - [ ] Model training procedures
   - [ ] Tool calling interfaces
   - [ ] Hardware specifications

3. **Which pattern involves self-reflection?**
   - [ ] ReAct
   - [ ] Plan-and-Solve
   - [ ] Reflexion

4. **How does an agent maintain context across interactions?**
   - [ ] Through memory stores
   - [ ] By retraining on each interaction
   - [ ] Using static configurations

*Answers available in `solutions/knowledge_check.md`*

---

## 🚀 Advanced Topics

### Tool Discovery and Registration

Implement dynamic tool registration:

```python
class ToolRegistry:
    """Dynamic tool registry with auto-discovery"""
    
    def __init__(self):
        self.tools = {}
        self.categories = {}
    
    def register(self, tool: MCPTool, categories: List[str] = None):
        self.tools[tool.name] = tool
        if categories:
            for cat in categories:
                self.categories.setdefault(cat, []).append(tool.name)
    
    def discover_tools(self, package_path: str):
        """Auto-discover tools from a package"""
        import importlib
        import pkgutil
        
        package = importlib.import_module(package_path)
        for _, name, _ in pkgutil.iter_modules(package.__path__, package.__name__ + "."):
            module = importlib.import_module(name)
            if hasattr(module, 'get_tools'):
                for tool in module.get_tools():
                    self.register(tool)
```

### Error Handling and Retry Logic

```python
import time
from functools import wraps

def retry_on_failure(max_attempts=3, delay=1.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                result = func(*args, **kwargs)
                if result.get("success"):
                    return result
                print(f"⚠️  Attempt {attempt+1} failed, retrying...")
                time.sleep(delay)
            return {"success": False, "error": "Max attempts reached"}
        return wrapper
    return decorator
```

---

## 📚 Additional Resources

### Documentation
- [MCP Specification](https://modelcontextprotocol.io/)
- [LangChain Agents](https://python.langchain.com/docs/modules/agents/)
- [AutoDoc Framework](https://github.com/microsoft/autogen)

### Videos
- [AI Agents Explained](https://youtube.com/example1)
- [Building Production Agents](https://youtube.com/example2)

### Tools & Libraries
- LangChain
- LlamaIndex
- AutoGen
- CrewAI

---

## ➡️ Next Steps

After completing this module:

1. ✅ Complete all lab exercises
2. ✅ Review knowledge check answers
3. ✅ Experiment with additional tools
4. ➡️ Proceed to [Day 09: RAG + Vector Databases](../day09-rag-vector-databases/)

---

**Need Help?** 
- Check [TROUBLESHOOTING.md](../../TROUBLESHOOTING.md)
- Join our [GitHub Discussions](https://github.com/your-repo/discussions)
- Review example solutions in `solutions/`
