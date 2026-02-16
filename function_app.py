"""
Optimus Agent Template - Azure Functions Implementation

An autonomous AI agent that wakes on schedule, processes tasks,
coordinates with MCP servers, and maintains state.

Built for Microsoft AI Dev Days Hackathon 2026
"""

import azure.functions as func
import datetime
import json
import logging
import os
from typing import Dict, Any, Optional

app = func.FunctionApp()

# Configuration
WAKE_SCHEDULE = "0 */15 * * * *"  # Every 15 minutes

class AgentState:
    """Manages agent state persistence."""

    def __init__(self, state_data: Optional[Dict] = None):
        self.wake_count = state_data.get("wake_count", 0) if state_data else 0
        self.last_wake = state_data.get("last_wake") if state_data else None
        self.active_tasks = state_data.get("active_tasks", []) if state_data else []
        self.capabilities = state_data.get("capabilities", {}) if state_data else {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "wake_count": self.wake_count,
            "last_wake": self.last_wake,
            "active_tasks": self.active_tasks,
            "capabilities": self.capabilities
        }

    def increment_wake(self):
        self.wake_count += 1
        self.last_wake = datetime.datetime.utcnow().isoformat()


class AgentCore:
    """Core agent logic - reasoning, planning, execution."""

    def __init__(self, state: AgentState):
        self.state = state
        self.logger = logging.getLogger("AgentCore")

    async def wake(self) -> Dict[str, Any]:
        """Execute a wake cycle."""
        self.state.increment_wake()

        results = {
            "wake_number": self.state.wake_count,
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "actions": [],
            "status": "healthy"
        }

        # Phase 1: Check for messages/commands
        messages = await self._check_messages()
        if messages:
            results["actions"].append(f"Processed {len(messages)} messages")

        # Phase 2: Execute pending tasks
        completed = await self._execute_tasks()
        if completed:
            results["actions"].append(f"Completed {len(completed)} tasks")

        # Phase 3: Self-improvement check
        improvements = await self._check_improvements()
        if improvements:
            results["actions"].append(f"Identified {len(improvements)} improvements")

        # Phase 4: Update metrics
        await self._update_metrics(results)

        return results

    async def _check_messages(self) -> list:
        """Check for incoming messages/commands."""
        # In production: integrate with Telegram, email, etc.
        return []

    async def _execute_tasks(self) -> list:
        """Execute pending tasks from the backlog."""
        completed = []
        for task in self.state.active_tasks:
            if task.get("status") == "pending":
                # Execute task based on type
                self.logger.info(f"Executing task: {task.get('name')}")
                completed.append(task.get("name"))
        return completed

    async def _check_improvements(self) -> list:
        """Identify potential self-improvements."""
        # Could integrate with GitHub Copilot for code suggestions
        return []

    async def _update_metrics(self, results: Dict):
        """Update telemetry and metrics."""
        self.logger.info(f"Wake {results['wake_number']}: {len(results['actions'])} actions")


@app.timer_trigger(schedule=WAKE_SCHEDULE,
                   arg_name="timer",
                   run_on_startup=False)
async def agent_wake(timer: func.TimerRequest) -> None:
    """
    Timer-triggered agent wake cycle.

    Runs every 15 minutes to:
    1. Check for new messages/commands
    2. Execute pending tasks
    3. Update state and metrics
    4. Report accomplishments
    """
    if timer.past_due:
        logging.warning("Wake cycle running late!")

    logging.info(f"Agent wake triggered at {datetime.datetime.utcnow()}")

    # Load state (in production: from Azure Blob Storage)
    state_data = _load_state()
    state = AgentState(state_data)

    # Execute wake cycle
    agent = AgentCore(state)
    results = await agent.wake()

    # Save state
    _save_state(state.to_dict())

    logging.info(f"Wake cycle completed: {json.dumps(results)}")


@app.route(route="status", methods=["GET"])
async def get_status(req: func.HttpRequest) -> func.HttpResponse:
    """
    HTTP endpoint to check agent status.

    Returns current state, recent activity, and health metrics.
    """
    state_data = _load_state()
    state = AgentState(state_data)

    status = {
        "status": "healthy",
        "wake_count": state.wake_count,
        "last_wake": state.last_wake,
        "active_tasks": len(state.active_tasks),
        "capabilities": list(state.capabilities.keys()),
        "version": "1.0.0"
    }

    return func.HttpResponse(
        json.dumps(status, indent=2),
        mimetype="application/json"
    )


@app.route(route="task", methods=["POST"])
async def add_task(req: func.HttpRequest) -> func.HttpResponse:
    """
    HTTP endpoint to add a new task.

    Accepts JSON body with task details.
    """
    try:
        task_data = req.get_json()

        if not task_data.get("name"):
            return func.HttpResponse(
                json.dumps({"error": "Task name required"}),
                status_code=400,
                mimetype="application/json"
            )

        state_data = _load_state()
        state = AgentState(state_data)

        task = {
            "id": len(state.active_tasks) + 1,
            "name": task_data.get("name"),
            "description": task_data.get("description", ""),
            "priority": task_data.get("priority", "normal"),
            "status": "pending",
            "created_at": datetime.datetime.utcnow().isoformat()
        }

        state.active_tasks.append(task)
        _save_state(state.to_dict())

        return func.HttpResponse(
            json.dumps({"success": True, "task": task}),
            mimetype="application/json"
        )

    except ValueError:
        return func.HttpResponse(
            json.dumps({"error": "Invalid JSON"}),
            status_code=400,
            mimetype="application/json"
        )


# State persistence helpers (use Azure Blob Storage in production)
_in_memory_state = {}

def _load_state() -> Dict:
    """Load agent state."""
    global _in_memory_state
    return _in_memory_state.copy()

def _save_state(state: Dict):
    """Save agent state."""
    global _in_memory_state
    _in_memory_state = state.copy()
