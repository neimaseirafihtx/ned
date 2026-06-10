---
name: mac-mini-m4
description: Mac Mini M4 — DECOMMISSIONED 2026-06-09, returned to store; replaced by [[windows-server]]
metadata:
  type: user
---

Mac Mini M4 (16GB) — **decommissioned and returned to the store 2026-06-09.** It no longer exists in the home lab. Do not suggest it as a host or troubleshoot it.

- Former role: primary always-on server (Hermes, HAOS-in-UTM, Ollama, Docker, Tailscale), static IP `192.168.68.85`, SSH alias `mac-mini` — all dead now.
- Hermes/Ray/Ollama migrated to the Windows server 2026-06-08 ([[windows-server]]).
- Home Assistant went offline with the Mini; restore on the Windows server is the next infra milestone. Recovery artifacts preserved at `C:\restore\home-assistant\backups\` (HA backup tar `automatic_backup_2026_5_4.tar` + ARM64 `haos.qcow2` + emergency kit notes); plan in `home-assistant-windows-migration-handoff-2026-06-08.md`.
- Any doc referencing `192.168.68.85`, `homeassistant.local:8123` via UTM, `en9`/UGREEN adapter, or macOS server setup is historical.

**Why:** prevents stale recommendations against a machine that was returned.
**How to apply:** treat all Mac Mini references in older docs/handoffs as history, not live infrastructure.
