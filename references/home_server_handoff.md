# Neima's Home Lab — Goals & Context

This is the source-of-truth context file for Ned. Update it as plans evolve.

## Hardware

### Mac Mini M4 — 16GB (PRIMARY SERVER, always on)
- Role: Home Assistant VM, Ollama, Frigate, Docker services
- M4 base chip, 16GB unified memory
- Already running with Docker installed

### M5 MacBook Pro (DEV MACHINE ONLY — not a server)
- Day-to-day development
- Does NOT run home lab services

### Windows Desktop — RTX GPU (PLANNED)
- Exact GPU TBD
- Primary role: local LLM inference offload once built
- Will run Ollama with CUDA for much faster inference

### Reolink 810A Cameras (CURRENT)
- 4K cameras, supports dual RTSP streams (main + sub)
- RTSP URLs: `h264Preview_01_main` (4K), `h264Preview_01_sub` (lower res)
- Default port 554

### Reolink NVR — RLN8-410 (PLANNED)
- 8-channel PoE NVR for local recording
- Will pull main stream from cameras
- Frigate will pull sub stream simultaneously (no conflict)

## Smart Home Devices

- **Lighting:** Philips Hue (multiple rooms), Lutron Caseta dimmers/switches
- **Thermostat:** Nest (Google account required for HA integration)
- **Audio:** Sonos (multiple speakers)
- **Cameras:** Reolink 810A (planned: 2-4 units)

## Project Phases

### Phase 1: Home Assistant ✅ PRIORITY
- Install HAOS in VM on Mac Mini (UTM recommended)
- Integrate: Hue → Caseta → Sonos → Nest (in that order)
- Nest requires Google Device Access Program setup ($5 fee)

### Phase 2: Local LLMs
- Install Ollama on Mac Mini
- Start with llama3.1:8b or phi3.5:3.8b for HA automation
- Add OpenWebUI for chat interface
- Connect to HA via Extended OpenAI Conversation (HACS)

### Phase 3: Cameras & Frigate
- Set up Reolink NVR for baseline recording
- Run Frigate on Mac Mini for AI detection
- Both NVR and Frigate pull from same cameras simultaneously
- Start without Coral TPU (software detection), add later if needed

### Phase 4: Remote Access
- Tailscale on Mac Mini + all devices
- Or Nabu Casa for HA-specific remote access

### Phase 5: Remote Desktop
- Remote into Mac Mini from anywhere
- Eventually remote into Windows desktop too

### Phase 6: Learning Lab
- Explore what the stack can do
- DIY sensors (ESPHome), custom automations, etc.

## Notes & Decisions Made

- **No REX on Mac Mini** — REX (separate project) runs on M1 Pro machine
- **Docker already installed** — starting point for all services
- **Priority: get HA working first** before LLMs or cameras
- **16GB is a real constraint** for local LLMs — don't try 32B models
- Local LLMs goal is HA automation + privacy, NOT replacing Claude
