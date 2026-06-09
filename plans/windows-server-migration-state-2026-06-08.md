# Windows Server Migration — Current State & Remaining Work
_Date: 2026-06-08 | Author: Ned/Claude Code session_

This document captures what is fully set up on the Windows PowerSpec, what remains to be done, and the complete Home Assistant migration plan. Created immediately before wiping the Mac Mini.

---

## What is set up and working right now

### Windows PowerSpec (primary server)

| Item | Status | Notes |
|------|--------|-------|
| OS | ✅ Windows 11 Pro (build 26200) | WMI reports "Windows 10 Pro" — that's a known display quirk, it's Win11 |
| Hostname | ✅ `Neima_Server` | User preference — not ned-server |
| LAN IP | ✅ `192.168.68.89` | Reserve in Deco if not already done |
| Tailscale | ✅ `100.120.157.4` / `neima-server` | On `neima.seirafi@gmail.com` tailnet |
| GPU | ✅ RTX 5060 Ti 16GB | `nvidia-smi` verified |
| RAM | ✅ 32GB DDR5 | |
| Git | ✅ v2.54 | |
| Python | ✅ 3.11 + 3.13 | 3.13 used by Hermes (SSH fix); 3.11 available |
| Ned repo | ✅ `C:\Users\neima\Documents\ned` | Cloned from GitHub |
| Claude Code | ✅ | Running in ned repo |

### Hermes / Ned

| Item | Status | Notes |
|------|--------|-------|
| Hermes | ✅ v0.16.0 | Home: `C:\Users\neima\AppData\Local\hermes\` |
| Model | ✅ GPT-5.5 via OpenAI Codex OAuth | |
| Telegram | ✅ Live | Gateway connected, test messages confirmed |
| Gateway persistence | ✅ Windows Scheduled Task `Hermes_Gateway` | Survives reboot |
| Memory / SOUL | ✅ MEMORY.md, USER.md, SOUL.md all present | 67 sessions carried over from Mac Mini |
| Config | ✅ v28 | Migrated + fixed from Mac Mini v26 |
| HA MCP config | ✅ Set to `http://192.168.68.85:8123/api/mcp` | Pointing at Mac Mini IP — update when HA moves to Windows |
| Cron jobs | ⚠️ Jobs exist, scripts missing | 3 jobs present; bash scripts will fail on Windows — rebuild needed |

**Hermes SSH caveat:** `hermes.cmd` points to system Python 3.13 instead of the venv to fix `os error 448` over SSH. If Hermes auto-updates and breaks SSH, re-apply the fix documented in `docs/windows-server-ssh-hermes-handoff.md` (inside migration bundle on Desktop).

### Ray Hermes

| Item | Status | Notes |
|------|--------|-------|
| Container | ✅ Running | `ray-hermes`, bound `100.120.157.4:8643→8642` |
| Data | ✅ `C:\hermes-friends\ray\` | `compose\`, `hermes-home\`, `workspace\` |
| Shared /shared | ✅ `C:\Users\neima\OneDrive\Ray Dropbox` | Live OneDrive-synced — must stay pinned "Always keep on this device" |
| Telegram | ✅ `@Trismegis_bot` | Ray Fitzgerald approved |
| Resources | ✅ `mem_limit: 2g`, `cpus: 2.0` | |
| Isolation | ✅ | No Neima home/HA/SSH/Docker socket access |

### Docker Desktop

| Item | Status | Notes |
|------|--------|-------|
| Docker Desktop | ✅ Installed, WSL2 backend | |
| Auto-start on login | ✅ Registry key present | |
| Minimize to tray on close | ⚠️ Needs manual toggle | Settings → General → "When closing Docker Desktop" → Minimize to system tray |

### Ollama

| Item | Status | Notes |
|------|--------|-------|
| Ollama | ✅ v0.30.7 | |
| Model | ✅ `gemma4:12b` (7.6GB) | 16GB VRAM gives good headroom |
| Hermes integration | 📋 Not configured yet | Don't make it the default model — set up as a separate local profile when needed |

---

## What still needs to be done

### Immediate / before next session

- [ ] **Wipe Mac Mini** — sign out of Apple ID first (System Settings → Apple ID → Sign Out)
- [ ] **Deco IP reservation** — reserve `192.168.68.89` for `Neima_Server` if not already done
- [ ] **Docker Desktop tray setting** — Settings → General → "When closing Docker Desktop" → Minimize to system tray
- [ ] **Reboot test** — reboot Windows server, confirm Hermes gateway, Docker, and Ray container all come back automatically

### Near-term

- [ ] **Rebuild cron scripts for Windows** — `mac-mini-health-brief.sh` and `ray-hermes-health-brief.sh` need to be rewritten as `.py` or `.ps1`. The Python update-check script works as-is. Until rebuilt, the two daily health briefs will fail silently each morning.
- [ ] **VS Code** — not installed yet (not in PATH). Download from `code.visualstudio.com`.
- [ ] **Delete migration bundle from Desktop** — `hermes-neima-migration-bundle-20260608T193416.tar.gz` and extracted folder contain API keys and Telegram token. Delete once you're satisfied everything is stable.

### Home Assistant migration (Phase 9 — intentionally last)

See full plan below and `home-assistant-windows-migration-handoff-2026-06-08.md` in this repo root.

---

## Home Assistant migration plan

### What we have saved

All HA restore artifacts are at: `C:\restore\home-assistant\backups\`

| File | What it is |
|------|-----------|
| `automatic_backup_2026_5_4.tar` | HA config backup from May 4 — restores integrations, dashboards, scenes, scripts. Config-only (4.5MB), not history. **This is the primary restore artifact.** |
| `haos.qcow2` | Full HAOS VM disk from Mac Mini (7GB, ARM64). Cannot boot directly on x86 Windows. Use as last-resort recovery only. |
| `home_assistant_backup_emergency_kit_6_8_2026_9_34 PM.txt` | Credentials/recovery info captured 2026-06-08 |
| `home-assistant-windows-migration-handoff-2026-06-08.md` | Full HA migration guide (also in ned repo root) |

Mac Mini migration backup (24GB) is on Google Drive as additional fallback.

### Recommended target: Hyper-V VM running HAOS x86_64

Do **not** use Docker Container as the primary. You lose add-ons, the official MCP Server integration, clean backup/restore, and supervisor features. Hyper-V is the right call on Windows 11 Pro.

Docker HA Container is fine for a quick test only.

### Phase-by-phase plan

**Phase 1 — Enable Hyper-V**
```powershell
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All
# Reboot when prompted
```
Verify: search "Hyper-V Manager" in Start.

Note: Docker Desktop uses WSL2 backend so Hyper-V and Docker Desktop coexist cleanly on Windows 11 Pro.

**Phase 2 — Create HAOS VM**
1. Download HAOS x86_64 `.vhdx` from: `https://www.home-assistant.io/installation/windows`
2. Open Hyper-V Manager → New → Virtual Machine:
   - Name: `HomeAssistant`
   - Generation: Generation 2
   - RAM: 4GB (static), 6-8GB if comfortable
   - Network: External virtual switch (bridged to `Ethernet` adapter for LAN visibility)
   - Disk: use the downloaded `.vhdx` directly
3. VM Settings → Security → disable Secure Boot (required for HAOS)
4. Boot the VM

**Phase 3 — Restore and configure**
1. On first boot, HA onboarding will offer to restore a backup — use `automatic_backup_2026_5_4.tar`
2. Reserve IP `192.168.68.68` in Deco for the new HA VM (keep the old IP to avoid breakage)
3. Verify in browser: `http://192.168.68.68:8123` or `http://homeassistant.local:8123`

**Phase 4 — Verify integrations**
After restore, confirm each of these:
- [ ] Philips Hue — all Family Room, Entryway, Listening Room lights
- [ ] Lutron Caseta — Master Bedroom, Dining Room, Kitchen, Exterior, Guestroom
- [ ] Sonos — Living Room, Listening Room, Office, Garage, Neima's Room
- [ ] Samsung TVs visible (control stays off-limits)
- [ ] Dashboard `Neima Home` at `/neima-home/home` exists
- [ ] Scripts: `script.family_room_evening`, `script.family_room_movie`, `script.all_house_lights_off`
- [ ] Official MCP Server integration installed and enabled

Scene targets to verify (from `references/home-assistant-script-drafts.yaml`):

_Evening:_ kitchen island pendants 30%, kitchen mains off, TV lightstrip 28%, family room lamp 75%, family room mains 1%, dining room 20%

_Movie:_ kitchen island pendants 35%, TV lightstrip 19%, family room lamp 25%, family room mains off, dining room off

**Phase 5 — Reconnect Hermes MCP**
1. In HA: Profile → Long-lived access tokens → Create new token for Hermes
2. Add to Windows Hermes `.env`: `HA_MCP_TOKEN=<new token>`
3. Update `C:\Users\neima\AppData\Local\hermes\config.yaml` MCP URL if IP changed:
```yaml
mcp_servers:
  homeassistant:
    url: http://192.168.68.68:8123/api/mcp
    headers:
      Authorization: Bearer ${HA_MCP_TOKEN}
    timeout: 120
    connect_timeout: 60
```
4. Restart Hermes gateway
5. Test: ask Hermes "what lights are on" — should return real state

**MCP safety boundary to preserve:**
- ✅ Read anything
- ✅ Control exact `light.*` entities and approved scripts
- ❌ Sonos / media players
- ❌ TVs
- ❌ HVAC / thermostat
- ❌ Locks / security / cameras
- ❌ Broad room-wide natural language targeting (use explicit entity IDs or named scripts)

**Phase 6 — Update cron scripts**
Replace Mac-specific health check scripts with Windows-aware versions. Deliver to main Telegram DM only (not Ned group).

### Key reference files in ned repo

| File | Purpose |
|------|---------|
| `references/home-assistant-entity-map.md` | Full entity list — use to verify IDs after restore |
| `references/home-assistant-automation-inventory.md` | Apple Home / Google Home / Hue / Lutron inventory |
| `references/home-assistant-script-drafts.yaml` | Exact YAML for Evening/Movie scenes and scripts |
| `plans/home-assistant-mcp-roadmap.md` | MCP architecture, safety rules, token setup |
| `plans/home-assistant-usability-pass.md` | Dashboard plan, room cards, scene targets |
| `home-assistant-windows-migration-handoff-2026-06-08.md` | Full migration guide with cutover checklist |

---

## Where everything lives

```
C:\restore\home-assistant\backups\     ← HA restore artifacts (qcow2 + backup tar + emergency kit)
C:\hermes-friends\ray\                 ← Ray Hermes Docker data
C:\Users\neima\AppData\Local\hermes\   ← Ned/Hermes home (config, state, memory, skills, cron)
C:\Users\neima\Documents\ned\          ← Ned repo (canonical project brain, shared with GitHub)
C:\Users\neima\OneDrive\Ray Dropbox\   ← Ray's shared file drop (must stay pinned local)
```

GitHub: `https://github.com/neimaseirafihtx/ned` — canonical source of truth for agent coordination

---

## Mac Mini — decommissioned 2026-06-08

- Hermes gateway: stopped ✅
- Ray Hermes container: stopped ✅  
- HAOS VM: left running briefly to confirm backup existed, then shut down
- Apple ID: sign out before wiping
- Mac Mini migration backup: on Google Drive as fallback
- After wipe: remove from Tailscale tailnet (Settings → remove device)
