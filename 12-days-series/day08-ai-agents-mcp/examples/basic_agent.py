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
            "parameters": self._get_param_schema(),
        }

    def _get_param_schema(self) -> Dict[str, Any]:
        return {}


class SearchTool(MCPTool):
    """Web search tool"""

    def __init__(self):
        super().__init__(
            name="search_web", description="Search the web for information"
        )

    def _get_param_schema(self) -> Dict[str, Any]:
        return {
            "query": {"type": "string", "description": "Search query"},
            "num_results": {
                "type": "integer",
                "description": "Number of results",
                "default": 5,
            },
        }

    def execute(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        # Simulated search (replace with actual API call)
        results = [f"Result {i+1} for '{query}'" for i in range(num_results)]
        return {
            "success": True,
            "results": results,
            "timestamp": datetime.now().isoformat(),
        }


class CalculatorTool(MCPTool):
    """Calculator tool for mathematical operations"""

    def __init__(self):
        super().__init__(
            name="calculate", description="Perform mathematical calculations"
        )

    def _get_param_schema(self) -> Dict[str, Any]:
        return {
            "expression": {"type": "string", "description": "Mathematical expression"}
        }

    def execute(self, expression: str) -> Dict[str, Any]:
        try:
            # Safe evaluation (in production, use proper parser)
            result = eval(expression, {"__builtins__": {}}, {})
            return {"success": True, "result": result, "expression": expression}
        except Exception as e:
            return {"success": False, "error": str(e)}


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
            return {"success": False, "error": f"Tool '{tool_name}' not found"}

        # Log the tool call
        call_record = {
            "type": "tool_call",
            "tool_name": tool_name,
            "parameters": kwargs,
            "context_id": self.context_id,
            "timestamp": datetime.now().isoformat(),
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
            "timestamp": datetime.now().isoformat(),
        }
        self.memory.append(result_record)

        return result

    def chat(self, user_input: str) -> str:
        """Process user input and respond"""
        # Simple keyword-based routing (replace with LLM in production)
        self.memory.append(
            {
                "type": "user_message",
                "content": user_input,
                "timestamp": datetime.now().isoformat(),
            }
        )

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
        if user_input.lower() == "quit":
            break

        response = agent.chat(user_input)
        print(f"Agent: {response}\n")

    print(f"\n📊 Session context saved: {len(agent.memory)} interactions")
