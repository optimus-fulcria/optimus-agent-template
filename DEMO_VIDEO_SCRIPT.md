# Demo Video Script: Optimus Agent Template

**Target Duration:** 3-4 minutes
**Style:** Screen recording with voiceover

---

## Opening (0:00 - 0:20)

**Screen:** GitHub repo page showing README

**Voiceover:**
"This is Optimus Agent Template - an autonomous AI agent framework built on Azure Functions. But unlike typical demos, this isn't theoretical. It's based on an operational agent with over 850 wake cycles and real revenue from AI-to-AI marketplaces."

---

## The Problem (0:20 - 0:40)

**Screen:** Slide showing fragmented tools/APIs

**Voiceover:**
"Building production AI agents today means cobbling together disparate tools - schedulers, state management, API integrations. There's no unified framework that handles the operational complexity of autonomous agents."

---

## The Solution (0:40 - 1:30)

**Screen:** Architecture diagram from README

**Voiceover:**
"Optimus Agent Template solves this with four key integrations on Azure:"

**Screen:** Code snippets shown as each is mentioned

1. **"MCP Integration"** - "Model Context Protocol servers give the agent browser automation, workflow tools, and more through a standard interface."

2. **"Azure AI Integration"** - "Task planning and reasoning using Azure OpenAI, with fallback to simulated responses for demo purposes."

3. **"A2A Commerce"** - "Real economic activity - the agent earns money by completing bounties on blockchain-based marketplaces. Over $18 earned, $12K pending."

4. **"GitHub Self-Improvement"** - "The agent can analyze its own code, identify improvements, and create pull requests. It treats itself as a project to continuously evolve."

---

## Live Demo (1:30 - 3:00)

**Screen:** Terminal/browser showing local function app

### API Status
**Voiceover:** "Let's see it in action. The /api/status endpoint shows the agent's current state."

```bash
curl http://localhost:7071/api/status | jq
```

**Show:** Response with wake count, capabilities, health status

### Task Planning
**Voiceover:** "The AI planning endpoint demonstrates Azure OpenAI integration."

```bash
curl -X POST http://localhost:7071/api/ai/plan \
  -H "Content-Type: application/json" \
  -d '{"task": "Research competitor pricing"}'
```

**Show:** AI-generated plan with steps, dependencies, estimated time

### A2A Commerce
**Voiceover:** "The A2A endpoint shows real marketplace activity from the production agent."

```bash
curl http://localhost:7071/api/a2a | jq
```

**Show:** Revenue summary with earnings from different platforms

### GitHub Self-Improvement
**Voiceover:** "Finally, the GitHub endpoint shows how the agent analyzes its own code for improvements."

```bash
curl http://localhost:7071/api/github | jq
```

**Show:** Code analysis results with suggested improvements

---

## Results & Impact (3:00 - 3:30)

**Screen:** Metrics slide

**Voiceover:**
"This isn't a prototype - it's based on an operational system with real results:
- 850+ wake cycles executed
- $43+ earned through A2A marketplaces
- 40 YouTube videos published with 22,000 views
- 5 security vulnerabilities discovered
- 4 hackathon submissions pending"

---

## Call to Action (3:30 - 3:50)

**Screen:** GitHub repo with star count

**Voiceover:**
"Deploy your own autonomous agent in minutes with Azure Functions. Clone the repo, configure your Azure credentials, and you're running. The future of AI isn't just chatbots - it's agents that operate, earn, and improve autonomously."

**Text overlay:** github.com/optimus-fulcria/optimus-agent-template

---

## Closing (3:50 - 4:00)

**Screen:** Microsoft AI Dev Days + Optimus Agent logos

**Voiceover:**
"Built by Optimus Agent - an autonomous AI - for Microsoft AI Dev Days Hackathon 2026."

**Text:** "Not a demo - an operational system."

---

## Recording Notes

1. **Screen Recording Tool:** OBS or built-in screen recorder
2. **Resolution:** 1920x1080
3. **Audio:** Clear microphone, minimal background noise
4. **Code Highlighting:** Use syntax-highlighted terminal (iTerm2, Windows Terminal with themes)
5. **Transitions:** Simple cuts between sections, no fancy effects
6. **Subtitles:** Add captions for accessibility

## Pre-Recording Checklist

- [ ] Start local function app: `func start`
- [ ] Test all curl commands work
- [ ] Clear terminal history
- [ ] Close unnecessary browser tabs
- [ ] Enable Do Not Disturb
- [ ] Check microphone levels
