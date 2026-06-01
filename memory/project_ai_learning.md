---
name: ai-learning
description: AI mastery is primary goal — Phase 3 active: HA+MCP, custom MCP server, first cron agent
metadata:
  type: project
---

AI agents and agentic workflows are the primary learning goal. Home lab is the sandbox, not the end goal.

**Current focus (Phase 3 — Connected Agents + MCP):**
1. Reboot Mac Mini → verify all services survive ✅
2. Clean HA entity map by room ✅
3. Enable HA MCP server → agents read live Home Assistant state ✅
4. Compare live MCP state against the curated entity map ✅
5. Build first custom MCP server (ned project/homelab status) ▶️ NEXT
6. First Hermes cron job — daily homelab health brief ▶️ NEXT
7. Define hybrid AI provider routing ▶️ NEXT
   - Hermes/OpenAI: primary always-on operator through current ChatGPT OAuth subscription
   - Claude: second-brain lane for plans, architecture, docs, code review, and careful review
   - Grok/xAI: possible extra cloud contingency if OAuth support proves stable in Hermes
   - Local Ollama/llama.cpp: simple summaries, log triage, structured extraction, HA intent parsing, privacy/offline fallback

**Current activation note:**
Hermes has crossed from chat-only into live tool-using home awareness: Home Assistant MCP read access works, the entity map is curated, and the first approved light write exposed the need for tighter exact-entity guardrails. Next lessons are custom MCP + scheduled autonomous reporting + explicit routing across OpenAI/Hermes, Claude, Grok/xAI contingencies, and local models so the right intelligence tier handles each task.

**Core concepts to master (in order):**
1. Agent loops — think → tool call → observe → repeat
2. Tool use / function calling — the primitive everything builds on
3. Memory systems — context window vs. persistent vs. session search
4. MCP — standardization layer; build at least one custom server yourself
5. Multi-agent orchestration — delegation, parallel workers
6. Skills / procedural memory — reusable captured workflows
7. Provider/model routing — decide when to use the Hermes/OpenAI primary cloud brain, Claude as reviewer/second brain, Grok/xAI as a contingency cloud lane, or local models as simple workers

**Key HA config notes (for when wiring Ollama to HA):**
- Use native Ollama integration (not HACS Extended OpenAI Conversation)
- Enable `prefer_local_intents: true` — HA handles simple intents, LLM only for complex
- Disable Qwen thinking mode in system prompt (`/no_think`) — voice/chat can't wait 20s
- HA Ollama endpoint: `localhost:11434` (same box as UTM VM)

**Key resources:**
- `references/Hermes Agent.md` — comprehensive Hermes internals
- `references/openclaw-notes.md` — OpenClaw/REX plugin API
- `plans/mac-mini-ops-baseline.md` — reboot verification checklist
