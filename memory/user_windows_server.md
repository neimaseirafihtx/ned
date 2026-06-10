---
name: windows-server
description: Windows PowerSpec — new primary Hermes/Ned host as of 2026-06-08; RTX 5060 Ti 16GB, 32GB RAM
metadata:
  type: user
---

PowerSpec PC — primary home lab server as of 2026-06-08. Replaced Mac Mini as Hermes host.

- **CPU:** Ryzen 7 7700X
- **GPU:** NVIDIA RTX 5060 Ti 16GB GDDR7
- **RAM:** 32GB DDR5
- **OS:** Windows 11 Pro (build 26200 — WMI reports "Windows 10 Pro" but it's Win11)
- **Hostname:** `Neima_Server` (user preference — not ned-server)
- **LAN IP:** `192.168.68.89`
- **Tailscale IP:** `100.120.157.4` / alias `neima-server`
- **SSH:** key auth from MBP via `ssh neima-server` alias

**Running services:**
- Hermes Agent v0.16.0 — GPT-5.5, Telegram connected, gateway installed as Windows Scheduled Task (`Hermes_Gateway`)
- Ray Hermes — Docker container, isolated, `@Trismegis_bot`, data at `C:\hermes-friends\ray\`
- Ollama v0.30.7 — `gemma4:12b` loaded, 16GB VRAM headroom
- Docker Desktop — WSL2 backend; set to start on login + minimize to tray on close
- Tailscale
- Claude Code at `C:\Users\neima\Documents\ned`

**Hermes home:** `C:\Users\neima\AppData\Local\hermes\`
**Ned repo:** `C:\Users\neima\Documents\ned`

**Known Hermes SSH caveat:** `hermes.cmd` points HERMES_PYTHON to system Python 3.13 (not venv) to fix SSH os error 448. If Hermes auto-updates and rewrites `hermes.cmd`, re-run the fix in `docs/windows-server-ssh-hermes-handoff.md` (also in the migration bundle on Desktop).

**HA MCP:** offline — the old endpoint pointed at the Mac Mini, which was decommissioned 2026-06-09 ([[mac-mini-m4]]). Re-point Hermes `HA_MCP_URL`/token after HA is restored here.

**Next up:**
- **Home Assistant restore on this machine** — Hyper-V HAOS x86_64 VM preferred (Docker Container is fallback only). Recovery artifacts staged at `C:\restore\home-assistant\backups\` (`automatic_backup_2026_5_4.tar`, ARM64 `haos.qcow2` — recovery artifact only, won't boot on x86), plus copies on OneDrive Desktop and `Downloads\mac-mini-migration-backups-...`. Full plan: `home-assistant-windows-migration-handoff-2026-06-08.md`.
- Cron bash scripts (`mac-mini-health-brief.sh`, `ray-hermes-health-brief.sh`) — rewrite as `.py` or `.ps1` for Windows host checks
- Gateway persistence confirmed via Scheduled Task; verify survives reboot
