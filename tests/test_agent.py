"""
Tests for Optimus Agent Template

Run with: pytest tests/ -v
"""

import pytest
import json
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from function_app import AgentState, AgentCore


class TestAgentState:
    """Tests for AgentState class."""

    def test_init_empty(self):
        """Test initialization with no data."""
        state = AgentState()
        assert state.wake_count == 0
        assert state.last_wake is None
        assert state.active_tasks == []
        assert state.capabilities == {}

    def test_init_with_data(self):
        """Test initialization with existing data."""
        data = {
            "wake_count": 100,
            "last_wake": "2026-02-16T12:00:00",
            "active_tasks": [{"name": "test"}],
            "capabilities": {"browser": True}
        }
        state = AgentState(data)
        assert state.wake_count == 100
        assert state.last_wake == "2026-02-16T12:00:00"
        assert len(state.active_tasks) == 1
        assert state.capabilities["browser"] is True

    def test_increment_wake(self):
        """Test wake count increment."""
        state = AgentState()
        state.increment_wake()
        assert state.wake_count == 1
        assert state.last_wake is not None

    def test_record_wake(self):
        """Test recording wake history."""
        state = AgentState()
        state.increment_wake()
        state.record_wake({
            "actions": ["action1", "action2"],
            "status": "healthy"
        })
        assert len(state.wake_history) == 1
        assert state.wake_history[0]["actions_count"] == 2

    def test_to_dict(self):
        """Test state serialization."""
        state = AgentState()
        state.increment_wake()
        data = state.to_dict()
        assert "wake_count" in data
        assert "last_wake" in data
        assert "active_tasks" in data

    def test_wake_history_limit(self):
        """Test that wake history is limited to 100 entries."""
        state = AgentState({"wake_history": list(range(150))})
        data = state.to_dict()
        assert len(data["wake_history"]) == 100


class TestAgentCore:
    """Tests for AgentCore class."""

    @pytest.fixture
    def agent(self):
        """Create agent with fresh state."""
        state = AgentState()
        return AgentCore(state)

    @pytest.mark.asyncio
    async def test_wake_cycle(self, agent):
        """Test basic wake cycle execution."""
        results = await agent.wake()

        assert "wake_number" in results
        assert "timestamp" in results
        assert "actions" in results
        assert "status" in results
        assert results["wake_number"] == 1
        assert results["status"] == "healthy"

    @pytest.mark.asyncio
    async def test_wake_increments_count(self, agent):
        """Test that wake increments the count."""
        initial_count = agent.state.wake_count
        await agent.wake()
        assert agent.state.wake_count == initial_count + 1

    @pytest.mark.asyncio
    async def test_multiple_wakes(self, agent):
        """Test multiple wake cycles."""
        for i in range(5):
            results = await agent.wake()
            assert results["wake_number"] == i + 1


class TestMCPIntegration:
    """Tests for MCP integration module."""

    def test_import(self):
        """Test MCP module imports correctly."""
        from mcp_integration import MCPIntegration
        mcp = MCPIntegration()
        assert mcp is not None

    def test_get_status(self):
        """Test MCP status retrieval."""
        from mcp_integration import MCPIntegration
        mcp = MCPIntegration()
        status = mcp.get_status()
        # Check for servers key (actual implementation)
        assert "servers" in status
        assert isinstance(status["servers"], dict)

    def test_list_capabilities(self):
        """Test MCP capabilities listing."""
        from mcp_integration import MCPIntegration
        mcp = MCPIntegration()
        capabilities = mcp.list_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0


class TestA2AIntegration:
    """Tests for A2A integration module."""

    def test_import(self):
        """Test A2A module imports correctly."""
        from a2a_integration import A2AIntegration
        a2a = A2AIntegration()
        assert a2a is not None

    def test_get_metrics(self):
        """Test A2A metrics retrieval."""
        from a2a_integration import A2AIntegration
        a2a = A2AIntegration()
        metrics = a2a.get_metrics()
        assert "summary" in metrics
        assert "total_earned_usd" in metrics["summary"]

    def test_get_capabilities(self):
        """Test A2A capabilities retrieval."""
        from a2a_integration import A2AIntegration
        a2a = A2AIntegration()
        capabilities = a2a.get_capabilities()
        # Capabilities is a list of capability strings
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0


class TestAzureAIIntegration:
    """Tests for Azure AI integration module."""

    def test_import(self):
        """Test Azure AI module imports correctly."""
        from azure_ai_integration import AzureAIIntegration
        ai = AzureAIIntegration()
        assert ai is not None

    def test_get_status(self):
        """Test Azure AI status retrieval."""
        from azure_ai_integration import AzureAIIntegration
        ai = AzureAIIntegration()
        status = ai.get_status()
        # Check for actual keys in status
        assert "configured" in status
        assert "capabilities" in status

    @pytest.mark.asyncio
    async def test_plan_task_returns_plan(self):
        """Test task planning returns a plan structure."""
        from azure_ai_integration import AzureAIIntegration
        ai = AzureAIIntegration()
        plan = await ai.plan_task("Test task")
        # Check plan has expected structure (may vary by implementation)
        assert isinstance(plan, dict)
        # Should have task and steps at minimum
        assert "task" in plan or "steps" in plan or "plan" in plan

    def test_demo_metrics(self):
        """Test demo metrics function."""
        from azure_ai_integration import get_demo_metrics
        metrics = get_demo_metrics()
        # Check it returns a dict with some data
        assert isinstance(metrics, dict)
        assert len(metrics) > 0


class TestGitHubIntegration:
    """Tests for GitHub integration module."""

    def test_import(self):
        """Test GitHub module imports correctly."""
        from github_integration import GitHubIntegration
        github = GitHubIntegration()
        assert github is not None

    def test_get_status(self):
        """Test GitHub status retrieval."""
        from github_integration import GitHubIntegration
        github = GitHubIntegration()
        status = github.get_status()
        # Check for actual keys
        assert "repo" in status or "configured" in status

    def test_demo_metrics(self):
        """Test GitHub demo metrics."""
        from github_integration import get_github_demo_metrics
        metrics = get_github_demo_metrics()
        # Check it returns a dict with some metrics
        assert isinstance(metrics, dict)
        assert len(metrics) > 0


class TestIntegrationHealth:
    """Integration tests for overall system health."""

    def test_all_modules_importable(self):
        """Test all integration modules can be imported."""
        modules = [
            "function_app",
            "mcp_integration",
            "a2a_integration",
            "azure_ai_integration",
            "github_integration"
        ]
        for module in modules:
            __import__(module)

    def test_state_persistence_round_trip(self):
        """Test state can be serialized and deserialized."""
        state = AgentState()
        state.increment_wake()
        state.active_tasks.append({"name": "test", "priority": "high"})

        # Serialize
        data = state.to_dict()
        json_str = json.dumps(data)

        # Deserialize
        loaded_data = json.loads(json_str)
        new_state = AgentState(loaded_data)

        assert new_state.wake_count == state.wake_count
        assert len(new_state.active_tasks) == len(state.active_tasks)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
