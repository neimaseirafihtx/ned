---
name: homelab-roadmap
description: Dual-track roadmap — AI mastery is primary goal, home lab is the sandbox; Phase 2 complete, Phase 3 active
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
| 1 | Agent Foundation | ✅ COMPLETE — Hermes + GPT-5.5 on Mac Mini, Telegram connected |
| 3 | Connected Agents + MCP | ▶️ ACTIVE — HA MCP, custom MCP server, ned as project brain |
| 5 | Multi-Agent & Autonomous Systems | 📋 Delegation, cron agents, skills library |
| 7 | Mastery + Sovereignty | 📋 Fully local stack, autonomous pipelines |

**Phase 3 detail (current focus):**
1. Reboot Mac Mini → verify all services survive (Hermes, HAOS, Ollama, Tailscale) ✅
2. Clean HA entity map — name everything by room/device
3. Enable official HA MCP Server integration → live read access is working; writes remain approval-gated
4. Compare live MCP state against `references/home-assistant-entity-map.md`
5. Build first custom MCP server (ned project/homelab status)
6. First Hermes cron job — daily homelab health brief

**Phase 3 deliverables:**
- `ned/plans/mac-mini-ops-baseline.md` — service startup verification
- `ned/plans/home-assistant-mcp-roadmap.md` — HA MCP install/validation plan with safety boundary and time estimates
- `ned/references/home-assistant-entity-map.md` — clean HA entity names
- Working: "ask Hermes what lights are on" → real answer ✅
- Working: daily health check cron agent

---

## Infrastructure Track (Enables AI Track)

| Phase | Name | Status |
|-------|------|--------|
| 2 | Home Lab Substrate | ✅ COMPLETE |
| 4 | Local Intelligence Layer | 📋 After Phase 3 — Frigate, NVR, Voice pipeline |
| 6 | GPU Stack | ⏸ Conditional — full Nest→Reolink migration only |

**Phase 2 complete state:**
- Mac Mini M4 16GB, macOS Tahoe 26.5, static IP `192.168.68.85`
- SSH key auth, auto-login, Homebrew, Tailscale, Screen Sharing ✅
- Docker Desktop (ARM native) ✅
- UTM + HAOS 17.3 at `homeassistant.local:8123` ✅
- Hue, Lutron Caseta, Sonos auto-discovered in HA ✅
- Ollama running with `qwen3.5:9b` ✅
- Hermes Agent running with GPT-5.5 backend + Telegram ✅
- ned repo on GitHub, shared between Claude Code + Hermes ✅

---

## 30-Day Plan (from 2026-05-29)

**Week 1 — Stabilize**
- Reboot Mac Mini, verify all services survive
- Document service startup state → `plans/mac-mini-ops-baseline.md`
- Confirm remote access from outside home via Tailscale

**Week 2 — HA Entity Cleanup**
- Name all entities by room/device consistently
- Add Nest if not a time sink
- Publish `references/home-assistant-entity-map.md`

**Week 3 — HA MCP + Agent Control**
- Enable official HA MCP Server integration with `Control Home Assistant` OFF for first read-only session
- Start read-only (list entities, read state)
- Add low-risk writes only after clean read-only validation (visible light/scene first)
- Deliverable: "ask Hermes what lights are on" → real answer

**Week 4 — Custom MCP + First Cron Agent**
- Build ned status MCP server (get_homelab_status, read_ned_memory, etc.)
- Add Hermes daily health brief cron job
- Save lessons as Hermes skill

---

## Key Decisions

- **AI learning is the primary goal** — home lab is the sandbox, not the destination
- **MCP is foundational** — invest in understanding it deeply, build custom servers
- **ned is the canonical project brain** — both Claude Code and Hermes read/write it via GitHub
- **Stabilize before expanding** — reboot test before adding new services
- **No cameras/Frigate yet** — rabbit hole, doesn't teach the core agent loop as directly as HA+MCP
- **No GPU stack yet** — only triggered by full Nest→Reolink migration
- **Camera migration rule** — keep Nest Aware until fully committing to local cameras
- **Ollama stays modest** — qwen3.5:9b for HA automation + light local use only
- **NVR owns camera storage** — external SSD is personal cloud only
- **No REX on Mac Mini** — REX runs on M1 Pro (separate project)
