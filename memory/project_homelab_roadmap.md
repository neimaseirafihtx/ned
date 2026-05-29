---
name: homelab-roadmap
description: Dual-track roadmap — AI mastery is primary goal, home lab is the sandbox. AI Track + Infrastructure Track.
metadata:
  type: project
---

## The Frame

AI agents and agentic workflows are the primary goal. The home lab is the live real-world sandbox agents operate in — not the end goal.

Two tracks run in parallel:

---

## AI Track (Primary)

| Phase | Name | Status |
|-------|------|--------|
| 1 | Agent Foundation | ✅ ACTIVE — Hermes running on MBP, GPT-5.5 backend |
| 3 | Connected Agents + MCP | 📋 Needs Mac Mini (HA MCP server, custom MCP servers, Nextcloud) |
| 5 | Multi-Agent & Autonomous Systems | 📋 Delegation, cron agents, skills library |
| 7 | Mastery + Sovereignty | 📋 Fully local stack, autonomous pipelines |

**Phase 1 detail:**
- Hermes Agent running on MBP with GPT-5.5 (OpenAI) ✅
- Goals: learn agent loop, tool use, memory systems, build first MCP server, write first skill
- REX (OpenClaw) on M1 Pro — separate project, cross-pollinate learnings
- Hermes moves to Mac Mini when it arrives

---

## Infrastructure Track (Enables AI Track)

| Phase | Name | Status |
|-------|------|--------|
| 2 | Home Lab Substrate | ⏳ Blocked — waiting on Mac Mini |
| 4 | Local Intelligence Layer | 📋 Frigate, NVR, Voice (Wyoming+Whisper+Piper), local Ollama backend |
| 6 | GPU Stack | ⏸ Conditional — only triggered by full Nest→Reolink camera migration |

**Phase 2 detail (Mac Mini arrival unlock):**
- UTM + HAOS VM → first live agent target
- Tailscale — agents reach home from anywhere
- Ollama lightweight model (llama3.1:8b or phi3.5) for HA automation
- Hermes Agent migrates here from MBP
- Integrate devices: Hue → Caseta → Sonos → Nest

---

## Key Decisions

- **AI learning is the primary goal** — home lab is the sandbox, not the destination
- **Hermes Agent is the primary learning vehicle** — understand its internals, not just use it
- **MCP is foundational** — invest in understanding it deeply
- **NVR owns camera storage** — external SSD is personal cloud only (Nextcloud + Backblaze B2)
- **No Synology needed** — NVR + SSD + Backblaze covers all storage
- **16GB Mac Mini LLM constraint** — max 8B model for HA automation only; heavy inference stays on MBP
- **Windows RTX is conditional, not planned** — only needed if fully replacing Nest cameras with Reolink (vision LLM needed to replace Nest Aware natural language descriptions)
- **Camera migration rule** — don't half-migrate; keep Nest Aware until fully committing to local cameras
- **No REX on Mac Mini** — REX runs on M1 Pro (separate project)
- **Confirmed tool stack** — Claude/Claude Code = primary tools, Hermes+GPT-5.5 = agent work, Mac Mini 8B = HA automation, Coral TPU = Frigate detection; MBP Ollama has no active use case
