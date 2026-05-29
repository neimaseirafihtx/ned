---
name: ai-learning
description: AI mastery is primary goal — Phase 3 active: HA+MCP, custom MCP server, first cron agent
metadata:
  type: project
---

AI agents and agentic workflows are the primary learning goal. Home lab is the sandbox, not the end goal.

**Current focus (Phase 3 — Connected Agents + MCP):**
1. Reboot Mac Mini → verify all services survive ✅
2. Clean HA entity map by room
3. Enable HA MCP server → endpoint/config in place; refresh token auth before relying on live reads
4. Compare live MCP state against the curated entity map after auth passes
5. Build first custom MCP server (ned project/homelab status)
6. First Hermes cron job — daily homelab health brief

**Core concepts to master (in order):**
1. Agent loops — think → tool call → observe → repeat
2. Tool use / function calling — the primitive everything builds on
3. Memory systems — context window vs. persistent vs. session search
4. MCP — standardization layer; build at least one custom server yourself
5. Multi-agent orchestration — delegation, parallel workers
6. Skills / procedural memory — reusable captured workflows

**Key HA config notes (for when wiring Ollama to HA):**
- Use native Ollama integration (not HACS Extended OpenAI Conversation)
- Enable `prefer_local_intents: true` — HA handles simple intents, LLM only for complex
- Disable Qwen thinking mode in system prompt (`/no_think`) — voice/chat can't wait 20s
- HA Ollama endpoint: `localhost:11434` (same box as UTM VM)

**Key resources:**
- `references/Hermes Agent.md` — comprehensive Hermes internals
- `references/openclaw-notes.md` — OpenClaw/REX plugin API
- `plans/mac-mini-ops-baseline.md` — reboot verification checklist
