---
name: mac-mini-m4
description: Mac Mini M4 16GB — active always-on server running HAOS/Ollama/Docker/Hermes; static IP 192.168.68.85
metadata:
  type: user
---

Mac Mini M4 — primary home lab server. Always on.

- **Chip:** Apple M4 (base)
- **RAM:** 16GB unified memory
- **OS:** macOS Tahoe 26.5 — use `launchctl enable` + `kickstart`, NOT `launchctl load` (deprecated in macOS 26)
- **Status:** Active — arrived 2026-05-28
- **Static IP:** `192.168.68.85`
- **SSH alias:** `mac-mini` (key auth, no password)
- **Username:** `neimaseirafi`

**Running services:**
- HAOS 17.3 in UTM VM → `homeassistant.local:8123` (Hue, Caseta, Sonos integrated)
- Ollama with `qwen3.5:9b` — HA automation + light local use
- Docker Desktop (ARM native)
- Hermes Agent (GPT-5.5 backend, Telegram connected)
- Tailscale → `neima.seirafi@gmail.com` tailnet

**Key constraint:** 16GB tight with Ollama (7.76GB) + UTM/HAOS (set to 2GB). OLLAMA_KEEP_ALIVE=0 recommended to unload model when idle.

**Planned additions:** Samsung T9 1TB SSD (Nextcloud), Google Coral TPU (Frigate), Reolink NVR (camera storage).

**ned repo:** cloned at `~/Documents/ned` — shared with Claude Code via GitHub.
