---
name: mac-mini-m4
description: Mac Mini M4 16GB — secondary/standby; Hermes migrated to Windows server 2026-06-08; still hosts HAOS VM
metadata:
  type: user
---

Mac Mini M4 — **no longer primary Hermes host as of 2026-06-08.** Hermes gateway stopped. Still online for HAOS.

- **Chip:** Apple M4 (base)
- **RAM:** 16GB unified memory
- **OS:** macOS Tahoe 26.5 — use `launchctl enable` + `kickstart`, NOT `launchctl load` (deprecated in macOS 26)
- **Static IP:** `192.168.68.85`
- **SSH alias:** `mac-mini` (key auth, no password)
- **Username:** `neimaseirafi`

**Current services (post-migration):**
- HAOS 17.3 in UTM VM → `homeassistant.local:8123` (Hue, Caseta, Sonos) — still active, HA not yet migrated to Windows
- Ray Hermes Docker container — migrated to Windows server 2026-06-08, Mac container stopped
- Hermes/Ned gateway — **stopped**, migrated to Windows server
- Ollama with `qwen3.5:9b` — still present but no active use case now that Hermes is on Windows
- Tailscale → `100.106.154.18`

**Planned:** HA will eventually move to Windows server (Hyper-V or Docker). Until then Mac Mini stays on as HA host only.

**ned repo:** cloned at `~/Documents/ned` — shared with Claude Code via GitHub.
