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
| 3 | Connected Agents + MCP | ▶️ ACTIVE — HA MCP read/live-state working; custom Ned MCP server + health cron are next |
| 5 | Multi-Agent & Autonomous Systems | 📋 Delegation, cron agents, skills library |
| 7 | Mastery + Sovereignty | 📋 Fully local stack, autonomous pipelines |

**Phase 3 detail (current focus):**
1. Reboot Mac Mini → verify all services survive (Hermes, HAOS, Ollama, Tailscale) ✅
2. Clean HA entity map — room/device map published and cross-checked ✅
3. Enable official HA MCP Server integration → live read access is working ✅; writes remain approval-gated
4. Compare live MCP state against `references/home-assistant-entity-map.md` ✅
5. Make Home Assistant useful for humans — automations, scenes, dashboards, and phone app setup ▶️ NEXT
6. Build first custom MCP server (ned project/homelab status) ▶️ NEXT
7. First Hermes cron job — daily homelab health brief ▶️ NEXT

**Phase 3 deliverables:**
- `ned/plans/mac-mini-ops-baseline.md` — service startup verification
- `ned/plans/home-assistant-mcp-roadmap.md` — HA MCP install/validation plan with safety boundary and time estimates
- `ned/references/home-assistant-entity-map.md` — clean HA entity names
- Working: "ask Hermes what lights are on" → real answer ✅
- Working: Home Assistant feels useful day-to-day, not just as an agent demo:
  - phone app installed/configured for Neima
  - useful rooms/dashboard/favorites surfaced
  - existing automations migrated/inventoried from Google Home, Lutron, and Hue
  - a first pass of scenes for common lighting states
  - a first pass of automations that beat Google Home / Apple Home for actual convenience
- Working: daily health check cron agent — not created yet; next activation step

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
- Reboot Mac Mini, verify all services survive ✅
- Document service startup state → `plans/mac-mini-ops-baseline.md` ✅
- Confirm remote access from outside home via Tailscale — still open

**Week 2 — HA Entity Cleanup**
- Name all entities by room/device consistently ✅
- Add Nest if not a time sink — deferred
- Publish `references/home-assistant-entity-map.md` ✅

**Week 3 — HA MCP + Agent Control**
- Enable official HA MCP Server integration with read-only-first safety boundary ✅
- Start read-only (list entities, read state) ✅
- Add low-risk writes only after clean read-only validation (visible light/scene first) ✅ first test completed; keep approval-gated
- Deliverable: "ask Hermes what lights are on" → real answer ✅

**Week 4 — Custom MCP + First Cron Agent + HA Usability**
- Build ned status MCP server (get_homelab_status, read_ned_memory, etc.)
- Add Hermes daily health brief cron job
- Make Home Assistant useful before expanding the stack:
  - install/configure Home Assistant Companion app on phone
  - create a simple mobile dashboard with the actually-used rooms/devices
  - inventory current automations/scenes from Google Home, Lutron, and Hue before recreating them in HA
  - define first scenes for common lighting states (Family Room, Entryway, Kitchen/Dining, Master Bedroom)
  - define first practical automations/notifications that Google Home / Apple Home do not already solve well
- Save lessons as Hermes skill

---

## Key Decisions

- **AI learning is the primary goal** — home lab is the sandbox, not the destination
- **Home Assistant must become useful, not ornamental** — prioritize automations, scenes, dashboards, and the phone app before adding more integrations; migrate/inventory existing Google Home, Lutron, and Hue automations so HA becomes the control plane instead of another parallel app; if it is worse than Google Home / Apple Home for daily use, the stack is not done
- **MCP is foundational** — invest in understanding it deeply, build custom servers
- **ned is the canonical project brain** — both Claude Code and Hermes read/write it via GitHub
- **Stabilize before expanding** — reboot test before adding new services
- **No cameras/Frigate yet** — rabbit hole, doesn't teach the core agent loop as directly as HA+MCP
- **No GPU stack yet** — only triggered by full Nest→Reolink migration
- **Camera migration rule** — keep Nest Aware until fully committing to local cameras
- **Ollama stays modest** — qwen3.5:9b for HA automation + light local use only
- **NVR owns camera storage** — external SSD is personal cloud only
- **No REX on Mac Mini** — REX runs on M1 Pro (separate project)
