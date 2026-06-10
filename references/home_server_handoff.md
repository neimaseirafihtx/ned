# Neima's Home Lab — Goals & Context

This is the source-of-truth context file for Ned. Update it as plans evolve.

> **MAJOR UPDATE (2026-06-09):** the home lab re-platformed. Hermes, Ray Hermes, and Ollama moved to the Windows PowerSpec server (`192.168.68.89`, see `memory/user_windows_server.md`) on 2026-06-08, and the Mac Mini was decommissioned and returned to the store on 2026-06-09. Home Assistant is **offline** until it's rebuilt on the Windows server (Hyper-V HAOS VM preferred; artifacts at `C:\restore\home-assistant\backups\`; plan in `home-assistant-windows-migration-handoff-2026-06-08.md`). Mac Mini details below are historical.

## The Goal

Build mastery of AI agents and agentic workflows. The home lab is the live real-world sandbox agents operate in — not the end goal, just the substrate. Two tracks run in parallel: **AI Track** (primary) and **Infrastructure Track** (enables AI track).

## Current Activation State

- **Roadmap status:** Phase 3 — Connected Agents + MCP is active.
- **What crossed the line:** Hermes can now read live Home Assistant state through MCP, not just reason from static docs.
- **What was learned:** Official HA MCP writes work, but targeting is natural-language/area-based; future agent writes should stay approval-gated or move behind an exact allowlisted wrapper.
- **Next milestone:** custom Ned MCP server for project/homelab status, then first Hermes daily health brief cron.
- **New roadmap item:** Docker-hosted friend Hermes pilot is queued after current Phase 3 work; see `plans/friend-hermes-docker-roadmap.md`.

## Hardware

### Mac Mini M4 — 16GB (DECOMMISSIONED 2026-06-09)
- Role (historical): always-on agent host, Home Assistant VM, Ollama, Docker services, personal cloud / agent workspace.
- Status: **decommissioned — returned to the store 2026-06-09**. Replaced by the Windows PowerSpec server.
- OS: macOS Tahoe 26.5.
- Static IP: `192.168.68.85`.
- Active LAN interface: `en9` via UGREEN USB-C 2.5GbE adapter, MAC `6c:1f:f7:c0:3e:e5`, verified at `2500Base-T <full-duplex>`.
- Running: Hermes Agent + Telegram gateway, HAOS 17.3 via UTM, Ollama `qwen3.5:9b`, Docker Desktop, Tailscale.
- Reboot finding: Hermes gateway, Tailscale, and Ollama auto-start; Docker Desktop may need `open -a Docker`; HAOS UTM VM named `Linux` may need `utmctl start 'Linux'` before `homeassistant.local:8123` returns 200.
- UTM recovery note: HAOS bridge must target `en9`, not stale built-in Ethernet `en0`, after the UGREEN adapter migration.

### MacBook Pro M5 Pro — 48GB (PRIMARY WORKSTATION)
- Personal laptop and primary development/workstation machine.
- Ollama installed: `qwen3.6:27b-mlx`, `qwen3.6:36b`.
- Hermes Agent has been removed from the MBP and moved to the Mac Mini.
- No active local-model use case right now; Claude + GPT-5.5 covers the current workflow unless offline/privacy-critical work appears.

### Windows Desktop — RTX GPU (CONDITIONAL / NOT PLANNED NOW)
- Role would be GPU inference offload and vision models if Neima fully migrates away from Nest cameras.
- Not a near-term project.

### Cameras / NVR
- Nest + Nest Aware remains active for now.
- Reolink/NVR/Frigate/local camera stack is a later project, not part of current activation.
- NVR should own camera storage if camera migration happens; Mac Mini external SSD is not for camera footage.

### External SSD / Storage
- Samsung T9 external SSD is the current direction for Mac Mini storage.
- Near-term role: personal storage, agent workspace, and potential future Nextcloud data drive.
- Not for NVR/camera footage.

## Network

- ISP: AT&T Fiber, 1 Gbps symmetrical.
- AT&T gateway model: **BGW320-500**.
- AT&T gateway Wi-Fi radios are off; setup is bridge/IP-passthrough-style into the home network.
- Main router/mesh node: TP-Link Deco BE63 connected over 2.5GbE.
- Downstream: 2.5GbE 8-port switch, three additional Deco nodes including one BE23, and a Luxul 16-port gigabit switch for home Ethernet.
- Mac Mini now uses UGREEN 2.5GbE adapter on `en9`; Deco reservation should remain tied to MAC `6c:1f:f7:c0:3e:e5` for `192.168.68.85`.
- Current network recommendation: keep Deco as Wi-Fi for now, but eventually add a dedicated gateway/router and move Deco into AP mode if/when segmentation/firewall/VPN control becomes important.

## Smart Home Devices

- **Lighting:** Philips Hue and Lutron Caseta.
- **Family Room lights:** user-facing “Family Room lights” means four entities: `light.family_room`, `light.family_room_lamp`, `light.tv_lightstrip`, and `light.family_room_main_lights`.
- **Audio:** Sonos speakers in multiple rooms.
- **TV/display:** Samsung Frame / OLED display entities show duplicate contexts in HA/MCP; prefer canonical entity IDs from `references/home-assistant-entity-map.md`.
- **Thermostat/cameras/security:** avoid writes unless explicitly scoped and approved.

---

## Roadmap

### Phase 1: Agent Foundation ✅ COMPLETE
**AI Track: learn the agent loop from the inside**
- Hermes Agent running with GPT-5.5 backend on the Mac Mini ✅
- Telegram connected ✅
- Ned repo shared through GitHub for Claude Code + Hermes alignment ✅
- Goals: tool use, memory systems, session search, skills, MCP, cron agents.

### Phase 2: Home Lab Substrate ✅ COMPLETE
**Infrastructure Track: stand up the real-world sandbox**
- Mac Mini M4 active ✅
- Tailscale / SSH / Homebrew / Screen Sharing baseline ✅
- UTM + HAOS 17.3 at `homeassistant.local:8123` ✅
- Hue, Lutron Caseta, Sonos discovered in Home Assistant ✅
- Ollama running with `qwen3.5:9b` ✅
- Docker Desktop installed ✅
- Hermes moved from MBP to Mac Mini ✅
- Reboot baseline documented in `plans/mac-mini-ops-baseline.md` ✅

### Phase 3: Connected Agents + MCP ▶️ ACTIVE
**AI Track: agents operating on real-world state**
- Official Home Assistant MCP Server installed and exposed at `/api/mcp` ✅
- Hermes native HTTP MCP config works under server name `homeassistant` ✅
- Read-only validation with `GetLiveContext` passed ✅
- `references/home-assistant-entity-map.md` cross-checked against live MCP state ✅
- First approved light write test completed ✅
- Write-control lesson: official HA MCP targeting can affect nearby/area lights; future writes stay approval-gated or move behind an exact allowlisted wrapper.
- **Next:** build custom Ned MCP server for project/homelab status.
- **Next:** create first Hermes daily health brief cron.

### Phase 4: Local Intelligence Layer 📋 LATER
**Infrastructure Track: reduce cloud dependency, add perception**
- Wyoming + Whisper (STT) + Piper (TTS) via HA Assist.
- Frigate on Mac Mini for AI object detection only if camera migration becomes active.
- Reolink NVR handles 24/7 recording if camera migration happens.
- Ollama remains modest on Mac Mini; heavy local model work belongs on stronger hardware.

### Phase 5: Multi-Agent & Autonomous Systems 📋 LATER
**AI Track: agents that run without you**
- Delegation patterns: orchestrator dispatching worker agents in parallel.
- Hermes cron jobs → autonomous agents running on schedule.
- Docker-hosted friend Hermes pilot: one isolated container/profile using the friend's own OpenAI OAuth, with strict volume/tool boundaries and no access to Neima's Hermes, Home Assistant, SSH keys, or home folder.
- Skills library: build reusable procedural memory, refine over time.
- Understand when to use single agent vs. multi-agent vs. just a tool call.

### Phase 6: GPU Stack + Vision ⏸ CONDITIONAL
**Infrastructure Track: serious local inference if camera migration justifies it**
- Windows RTX or other CUDA box only if full Nest→Reolink migration requires local vision LLM capability.
- Not part of the near-term roadmap.

### Phase 7: Mastery + Sovereignty 📋 LATER
**Both tracks converge**
- Fully local AI stack where practical: local inference, local data, local agents, no required cloud for core workflows.
- ESPHome DIY sensors feeding real-time context into agent pipelines.
- Autonomous home pipelines operating without intervention.
- Personal skills library and workflow tooling refined to daily use.

---

## Notes & Decisions Made

- **AI learning is the primary goal** — home lab is the sandbox, not the destination.
- **Hermes Agent is the primary learning vehicle** — study its internals, not just use it.
- **MCP is foundational** — invest in understanding it deeply, not just wiring it up.
- **Ned is the canonical project brain** — Claude Code and Hermes should both read/write this repo.
- **No REX on Mac Mini** — REX runs on M1 Pro / separate project context.
- **16GB Mac Mini LLM constraint** — keep local models modest; heavy inference stays elsewhere.
- **No cameras/Frigate yet** — do not start that rabbit hole before Phase 3 custom MCP + cron work lands.
- **NVR owns camera storage** — external SSD is personal cloud / agent workspace only.
- **Official HA MCP writes remain approval-gated** until exact control wrappers or HA groups make targeting safe.
- **Friend Hermes hosting is a pilot, not a hardware trigger yet** — start with one Docker-isolated OpenAI OAuth container on the Mac Mini when ready; reassess hardware only after measuring real memory/CPU pressure.
