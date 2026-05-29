---
name: ai-learning
description: AI mastery is Neima's primary goal — agents, agentic workflows, MCP, Hermes Agent internals
metadata:
  type: project
---

AI agents and agentic workflows are the primary learning goal. Home lab is the sandbox, not the end goal.

**Why:** Neima wants to be at the frontier — understanding how agent loops work, how MCP connects everything, how multi-agent systems coordinate. Not just using tools but mastering the underlying architecture.

**Current state (2026-05-25):**
- Hermes Agent running on MBP with GPT-5.5 backend ✅ — Phase 1 AI Track active
- REX (OpenClaw) running on M1 Pro — separate but related
- Next steps: build first custom MCP server, write first Hermes skill, study `run_conversation()` loop

**Core concepts to master (in order):**
1. Agent loops — think → tool call → observe → repeat
2. Tool use / function calling — the primitive everything builds on
3. Memory systems — context window vs. persistent vs. FTS5 session search
4. MCP — standardization layer for portable tools
5. Multi-agent orchestration — delegation, parallel workers, orchestrator/worker patterns
6. Skills / procedural memory — reusable captured workflows

**Key resources:**
- `references/Hermes Agent.md` — comprehensive Hermes internals reference
- `references/openclaw-notes.md` — OpenClaw/REX setup and plugin API
- Hermes source: `run_agent.py` → `run_conversation()` is the canonical agent loop
