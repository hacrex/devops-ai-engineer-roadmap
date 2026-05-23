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
