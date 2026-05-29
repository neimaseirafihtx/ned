# Neima's Home Lab — Goals & Context

This is the source-of-truth context file for Ned. Update it as plans evolve.

## The Goal

Build mastery of AI agents and agentic workflows. The home lab is the live real-world sandbox agents operate in — not the end goal, just the substrate. Two tracks run in parallel: **AI Track** (primary) and **Infrastructure Track** (enables AI track).

## Hardware

### Mac Mini M4 — 16GB (PRIMARY SERVER)
- Role: always-on agent host, Home Assistant VM, Ollama, Frigate, Docker services, personal cloud
- M4 base chip, 16GB unified memory, Docker installed
- Status: **ordered, not yet arrived**

### MacBook Pro M5 Pro — 48GB (PRIMARY WORKSTATION)
- Personal laptop and current AI experimentation machine
- Ollama: `qwen3.6:27b-mlx`, `qwen3.6:36b`
- Open WebUI running
- **Hermes Agent running** — GPT-5.5 (OpenAI) as backend ✅
- Hermes moves to Mac Mini once it arrives
- Status: **active**

### Windows Desktop — RTX GPU (PLANNED)
- Exact GPU TBD
- Role: GPU inference offload (CUDA), vision models on camera feeds
- CUDA inference is 3-5x faster than Apple Silicon at same model size

### Reolink 810A Cameras (ON HAND)
- 4K cameras, dual RTSP streams (main + sub)
- RTSP: `h264Preview_01_main` (4K), `h264Preview_01_sub` (lower res), port 554

### Reolink NVR — RLN8-410 (PLANNED)
- Handles ALL camera storage/recording — main stream, 24/7
- Frigate pulls sub stream simultaneously for AI detection only
- NVR owning storage = Mac Mini SSD is NOT for camera footage

### External SSD — 1-2TB (PLANNED)
- Mac Mini via USB/Thunderbolt
- Role: personal cloud (Nextcloud), Docker volumes
- Not for camera footage

## Smart Home Devices

- **Lighting:** Philips Hue (multiple rooms), Lutron Caseta dimmers/switches
- **Thermostat:** Nest (Google Device Access Program required for HA — $5 fee)
- **Audio:** Sonos (multiple speakers)
- **Cameras:** Reolink 810A (planned: 2-4 units)

---

## Roadmap

### Phase 1: Agent Foundation ✅ ACTIVE — running on MBP now
**AI Track: learn the agent loop from the inside**
- Hermes Agent running with GPT-5.5 backend ✅
- Goals: tool use, memory systems, session search, skills
- Build first custom MCP server (simple, real use case)
- Create first custom skill
- REX (OpenClaw) also running on M1 Pro — cross-pollinate learnings
- Study Hermes architecture: `run_conversation()` is the canonical agent loop

### Phase 2: Home Lab Substrate ⏳ Blocked on Mac Mini
**Infrastructure Track: stand up the real-world sandbox**
- UTM + HAOS VM on Mac Mini — first live agent target
- Tailscale on all devices — agents can reach home from anywhere
- Ollama on Mac Mini: lightweight model (llama3.1:8b or phi3.5:3.8b) for HA automation
- Integrate devices: Hue → Caseta → Sonos → Nest (in that order)
- Move Hermes Agent from MBP to Mac Mini

### Phase 3: Connected Agents + MCP
**AI Track: agents operating on real-world state**
- HA MCP server → Hermes and Claude controlling home via structured tool calls
- Build custom MCP servers for personal workflows (beyond HA)
- Claude Desktop → HA: direct control today, no extra setup
- Nextcloud in Docker + 1-2TB external SSD → personal data layer
- Backblaze B2 (~$6/mo) for offsite backup — no Synology needed
- Agents operating on your own files, not cloud silos

### Phase 4: Local Intelligence Layer
**Infrastructure Track: reduce cloud dependency, add perception**
- Wyoming + Whisper (STT) + Piper (TTS) via HA Assist → fully local voice pipeline
- Frigate on Mac Mini for AI object detection (sub stream only)
- Reolink NVR handling 24/7 recording (main stream)
- Ollama as local agent backend — full agent pipelines with no cloud calls

### Phase 5: Multi-Agent & Autonomous Systems
**AI Track: agents that run without you**
- Delegation patterns: orchestrator dispatching worker agents in parallel
- Hermes cron jobs → autonomous agents running on schedule
- Skills library: build reusable procedural memory, refine over time
- Understand when to use single agent vs. multi-agent vs. just a tool call

### Phase 6: GPU Stack + Vision *(Windows RTX arrives)*
**Infrastructure Track: serious local inference**
- Windows RTX running Ollama with CUDA — 3-5x speed over Apple Silicon
- Vision models (LLaVA/similar) analyzing camera feeds beyond Frigate detection
- Heavy model experiments that 16GB Mac Mini can't run
- Full local LLM stack capable of real workloads

### Phase 7: Mastery + Sovereignty
**Both tracks converge**
- Fully local AI stack: local inference, local data, local agents, no required cloud
- ESPHome DIY sensors feeding real-time context into agent pipelines
- Autonomous home pipelines operating without intervention
- Personal skills library and workflow tooling refined to daily use
- Remote desktop into Mac Mini and Windows from anywhere

---

## Notes & Decisions Made

- **AI learning is the primary goal** — home lab is the sandbox, not the end goal
- **Hermes Agent is the primary learning vehicle** — study its internals, not just use it
- **MCP is foundational** — invest in understanding it deeply, not just wiring it up
- **No REX on Mac Mini** — REX runs on M1 Pro (separate project)
- **16GB Mac Mini LLM constraint** — max 8B model; heavy inference stays on MBP or Windows RTX
- **NVR owns camera storage** — external SSD is personal cloud only
- **No Synology needed** — NVR + SSD + Backblaze B2 covers all storage
- **Hermes moves to Mac Mini** when it arrives — MBP stays as dev/experimentation machine
- **Local LLMs on Mac Mini = HA automation + agent backend**, not replacing Claude
