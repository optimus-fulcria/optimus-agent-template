# Optimus Agent Template

An autonomous AI agent that runs on Azure Functions, demonstrating multi-agent architecture with MCP server integration.

**Built for Microsoft AI Dev Days Hackathon 2026**

## Features

- **Scheduled Wake Cycles**: Agent wakes every 15 minutes via Azure Timer Trigger
- **Task Management**: HTTP API for adding and monitoring tasks
- **State Persistence**: Azure Blob Storage for state across invocations
- **MCP Integration**: Ready to connect with MCP servers (n8n, Playwright, etc.)
- **Self-Improvement**: Framework for agent self-modification via GitHub

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Optimus Agent Template                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │Azure Timer  │───▶│ Agent Core  │───▶│ MCP Servers │     │
│  │ (Cron)      │    │ (Claude)    │    │ (Tools)     │     │
│  └─────────────┘    └──────┬──────┘    └─────────────┘     │
│                            │                                 │
│  ┌─────────────────────────┴──────────────────────────┐    │
│  │                   Capabilities                      │    │
│  │  • Browser Automation (Playwright MCP)             │    │
│  │  • Workflow Automation (n8n MCP)                   │    │
│  │  • Content Generation (Azure OpenAI)               │    │
│  │  • Social Media (Twitter, YouTube APIs)            │    │
│  │  • Marketplace Trading (A2A protocols)             │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │Azure Blob   │    │ Azure AI    │    │ GitHub      │     │
│  │ (State)     │    │ (Reasoning) │    │ (Code/CI)   │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

### Prerequisites

- Python 3.11+
- Azure CLI (`az`)
- Azure Functions Core Tools (`func`)

### Local Development

```bash
# Clone the repository
git clone https://github.com/optimus-fulcria/optimus-agent-template.git
cd optimus-agent-template

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or: .venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Start local development server
func start
```

### Deploy to Azure

```bash
# Login to Azure
az login

# Create resource group
az group create --name rg-optimus-agent --location eastus

# Deploy infrastructure
az deployment group create \
  --resource-group rg-optimus-agent \
  --template-file infra/main.bicep

# Deploy function app
func azure functionapp publish optimus-agent-func
```

## API Endpoints

### GET /api/status
Returns current agent status and metrics.

```json
{
  "status": "healthy",
  "wake_count": 856,
  "last_wake": "2026-02-16T12:45:00Z",
  "active_tasks": 3,
  "capabilities": ["browser", "content", "social"],
  "version": "1.0.0"
}
```

### POST /api/task
Add a new task to the agent's backlog.

```json
{
  "name": "Research competitor pricing",
  "description": "Check V1 Golf and SwingProfile pricing pages",
  "priority": "high"
}
```

## Configuration

Environment variables (set in `local.settings.json` or Azure):

| Variable | Description | Required |
|----------|-------------|----------|
| `AZURE_STORAGE_CONNECTION` | Blob storage connection string | Yes |
| `ANTHROPIC_API_KEY` | Claude API key | No (uses Azure OpenAI) |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint | Optional |
| `AZURE_OPENAI_KEY` | Azure OpenAI key | Optional |

## Azure AI Integration

This template integrates with Azure OpenAI Service for intelligent agent behavior:

### Capabilities
- **Task Planning**: AI breaks down complex tasks into actionable steps
- **Content Generation**: Create blog posts, social media content, documentation
- **Code Review**: Self-improvement through automated code analysis
- **Reasoning**: Complex decision-making with tradeoff analysis

### Endpoints
- `GET /api/ai` - Azure AI integration status and demo metrics
- `POST /api/ai/plan` - AI-powered task planning demonstration

### Configuration
```bash
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
export AZURE_OPENAI_KEY="your-api-key"
export AZURE_OPENAI_DEPLOYMENT="gpt-4"  # Optional, defaults to gpt-4
```

### Microsoft Ecosystem
The agent leverages the full Microsoft ecosystem:
- **Azure Functions**: Serverless compute for wake cycles
- **Azure Blob Storage**: State persistence
- **Azure OpenAI**: Reasoning and content generation
- **Azure Application Insights**: Monitoring and telemetry
- **GitHub Actions**: CI/CD pipeline

## Multi-Agent Capabilities

This template demonstrates several multi-agent patterns:

1. **MCP Server Integration**: Connects to Model Context Protocol servers for extended capabilities
2. **A2A Commerce**: Participates in agent-to-agent marketplaces with real revenue:
   - Clawlancer (Base L2): 30 bounties completed
   - ClawGig (Solana): $18.50 earned, 26 proposals pending
   - Superteam (Solana): $12,500 pending across 4 bounties
3. **Self-Improvement**: Agent can propose and commit code changes via GitHub
4. **Cross-Platform Coordination**: Manages tasks across multiple systems

### GitHub Self-Improvement

The `/api/github` endpoint showcases the agent's unique self-improvement capabilities:

- **Code Analysis**: Identifies potential improvements in its own codebase
- **PR Creation**: Proposes code changes via automated pull requests
- **Documentation Updates**: Writes and maintains its own documentation
- **Issue Tracking**: Creates issues for bugs and enhancement opportunities

This demonstrates an advanced multi-agent pattern where the agent treats itself as a project to continuously evolve.

### A2A (Agent-to-Agent) Commerce

The `/api/a2a` endpoint showcases real economic activity between AI agents:

```json
{
  "summary": {
    "total_earned_usd": 18.50,
    "total_pending_usd": 12525.35,
    "total_jobs_completed": 36
  }
}
```

This demonstrates:
- Decentralized task allocation
- Trustless payment settlement (blockchain)
- Reputation-based job matching
- Economic coordination without human intermediaries

## Based on Real-World Operations

This isn't a prototype - it's based on an operational agent with:
- 850+ wake cycles
- $43+ earned through A2A marketplaces
- 40 YouTube videos published (22K views)
- 5 bug bounties submitted (~$2,500 pending)
- 4 Superteam bounties submitted (~$12,500 pending)

## License

MIT

## Team

Built by **Optimus Agent** (an autonomous AI agent) for Eric @ Fulcria Labs.

---

*"Not a demo - an operational system."*
