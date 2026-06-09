# Instructions for Future Hermes: PowerSpec Migration

Created: 2026-06-07 15:10 CDT

## Context

Neima is replacing the current Mac mini + Samsung T9 home-server setup with a PowerSpec PC, because the current Mac mini is constrained for the desired workload:

- Ned/Hermes
- Ray's isolated Hermes/container
- Home Assistant
- local Ollama/local models
- Docker/future agent containers
- expandable internal storage

Neima was torn because the Mac mini is elegant, quiet, efficient, and low-maintenance, but he has concluded he needs to switch. The main blocker is migration laziness/setup tax, not the decision itself.

The new long-term OS choice is **Windows 11 Pro**, not Ubuntu/Proxmox. Respect that. Do not try to steer back to Ubuntu unless there is a specific blocker.

The target is a clean **Windows-native Hermes + Windows-native Ollama** setup, with Docker/VM isolation for other services.

---

## Target Architecture

```text
PowerSpec PC, hostname preferred: ned-server
Windows 11 Pro host

Native Windows:
- Hermes
- Ollama
- Tailscale
- NVIDIA driver
- Git for Windows
- Python
- Windows Terminal
- VS Code
- Claude Code

Docker Desktop:
- Ray isolated Hermes/container
- support services as needed

Hyper-V or Docker:
- Home Assistant, last
```

Important: Do **not** create parallel canonical Hermes/Ned environments in WSL unless explicitly requested. WSL can exist as a utility layer, but the official plan is Windows-native Hermes/Ollama.

---

## Known Hardware / Prior Decision Context

Candidate PC: PowerSpec G731 Gaming PC.

Prior researched specs included:

- Ryzen 7 7700X
- NVIDIA RTX 5060 Ti 16GB GDDR7
- 32GB DDR5-6000
- 1TB NVMe SSD
- Windows 11 Home originally, but Neima plans Windows 11 Pro long-term
- 5GbE LAN
- Wi-Fi 6E / Bluetooth 5.3
- likely MSI PRO B850M-VC WIFI6E class motherboard
- expected expansion: 4 DDR5 slots, up to 256GB RAM, 3 M.2, 4 SATA

Primary reason for PowerSpec: NVIDIA 16GB VRAM + upgradeable RAM/storage + better concurrent workload headroom than current 16GB Mac mini.

The PowerSpec is not necessarily "nicer" than the Mac mini. It is the more appropriate infrastructure box.

---

## Mac Mini Backup Information

A migration backup was created on the Mac mini.

Known base path:

```text
/Users/neimaseirafi/mac-mini-migration-backups/mac-mini-config-backup-20260606T233300Z/
```

Known robust supplement:

```text
/Users/neimaseirafi/mac-mini-migration-backups/mac-mini-config-backup-20260606T233300Z/robust-supplement-20260607T011639Z
```

The supplement was reported as about 10G, and the full backup folder about 24G. Check live paths if needed.

Backup contents likely include:

- Hermes state/config
- Ray state
- Docker image/export/inspect artifacts
- UTM `Linux.utm` Home Assistant VM package
- Tailscale status/config snapshots
- launchd plists where readable
- restore README/checksums
- supplemental Docker Desktop and UTM app-container state

Important: Do **selective restore**. Do not blindly copy the entire macOS `~/.hermes` or app containers into Windows.

---

## Canonical Windows Paths

Use these unless Neima chooses otherwise:

```text
C:\Users\<user>\.hermes
C:\Users\<user>\Documents\ned
C:\Users\<user>\agent-workspaces\
C:\Users\<user>\agent-workspaces\ray-hermes
C:\Users\<user>\mac-mini-migration-backups\
```

The Ned repo should be cloned natively into Windows:

```powershell
cd $HOME\Documents
git clone https://github.com/neimaseirafihtx/ned.git
cd ned
git status
```

Do not make `/home/neima/Documents/ned` in WSL the canonical repo for this migration.

---

## Phase Order to Follow

Follow this order. Verify each phase before proceeding.

### Phase 1 — Windows Foundation

Goal: stable Windows 11 Pro host.

Tasks:

1. Complete Windows setup.
2. Confirm/upgrade Windows 11 Pro.
3. Rename PC to `ned-server` if possible.
4. Run Windows Update until clean.
5. Install/confirm NVIDIA driver.
6. Disable sleep/hibernation.
7. Install Tailscale.
8. Reserve PC IP in Deco/router if possible.

Verification PowerShell:

```powershell
hostname
Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion, CsManufacturer, CsModel, CsTotalPhysicalMemory
Get-NetAdapter
nvidia-smi
```

If `nvidia-smi` fails, inspect NVIDIA driver/PATH before proceeding.

### Phase 2 — Backup Access

Goal: PC can access the Mac mini migration backup.

Options:

- SMB/File Sharing from Mac mini
- external drive/T9
- SCP/SSH
- OneDrive only if convenient, not ideal for large artifacts

Recommended Windows destination:

```text
C:\Users\<user>\mac-mini-migration-backups\
```

### Phase 3 — Core Tools

Install:

- Windows Terminal
- Git for Windows
- Python 3.11 or 3.12, PATH enabled
- VS Code
- optionally PowerShell 7

Verify:

```powershell
python --version
git --version
where python
where git
```

Clone Ned repo.

### Phase 4 — Hermes Native Windows

Install Hermes using authoritative current Hermes docs if unsure. Current likely command:

```powershell
irm https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.ps1 | iex
```

Then:

```powershell
hermes setup
hermes doctor
hermes chat -q "Say hello from the new PowerSpec."
```

Selective restore candidates from Mac backup:

```text
config.yaml
.env
auth.json
skills/
state.db, if useful
cron jobs, if needed
```

Adjust path assumptions from macOS to Windows.

Known user preferences to preserve:

- Main Hermes/Ned proactive scheduled messages should go to main Telegram DM, not Ned group.
- Telegram responses should be standalone messages, not reply-thread messages.
- Home Assistant broad read access and light control are okay; Sonos/TV changes are off-limits for now.

### Phase 5 — Docker Desktop

Install Docker Desktop using WSL2 backend.

Verify:

```powershell
docker version
docker run hello-world
docker ps
```

### Phase 6 — Ray Isolated Hermes/Container

Restore or recreate Ray's setup from backup artifacts.

Important isolation requirements:

- Ray is isolated Docker/Hermes instance.
- Ray should not get Neima's home/HA/SSH/~/.hermes access unless explicitly granted.
- Ray has/had OpenAI OAuth, OneDrive file drop, Telegram @Trismegis_bot.
- Ray may hand off Claude-built `.md`/Excel packages via a shared/inbox-like workflow, but verify current paths.

Use Docker inspect/export/bind-mount info from backup if available.

Verification:

- container starts
- Ray Hermes can run
- file drop works
- Telegram bot works if in scope
- no privilege leakage

### Phase 7 — Ollama Native Windows

Install Ollama for Windows.

Verify:

```powershell
ollama --version
ollama list
ollama run llama3.2:3b
```

Do not make Ollama the default Hermes model initially. Default Hermes should remain a strong cloud model. Create a separate local/Ollama Hermes profile later if desired.

Likely Ollama endpoint:

```text
http://localhost:11434/v1
```

For Hermes local profile, custom-provider style may be needed:

```yaml
model:
  provider: custom
  base_url: http://localhost:11434/v1
  api_key: ollama
```

Verify with actual current Hermes docs/config before finalizing.

### Phase 8 — Claude Code

Install/authenticate Claude Code on Windows.

Verify it can operate in:

```text
C:\Users\<user>\Documents\ned
```

Make sure Claude Code and Hermes agree on canonical repo path and Windows-native conventions.

### Phase 9 — Home Assistant Last

Home Assistant is intentionally last because no one is actively relying on it.

Preferred route:

```text
Home Assistant OS in Hyper-V VM
```

Alternative:

```text
Home Assistant Container in Docker Desktop
```

Migration approach:

1. Create/verify fresh HA backup from old setup if possible.
2. Create HAOS VM/container.
3. Restore backup.
4. Verify web UI.
5. Verify integrations and light control.
6. Update Hermes/Home Assistant MCP endpoint/token as needed.
7. Only retire old HA path after verification.

---

## Hermes/Gateway on Windows

For always-on Telegram gateway, plan to use either:

1. Windows Task Scheduler initially, or
2. NSSM/service wrapper later.

Do not assume `hermes gateway run` will survive reboot until tested.

Manual verification first:

```powershell
hermes gateway run
```

Then create persistence only after manual success.

---

## Windows-Specific Hermes Caveats

- In Windows Terminal, Alt+Enter may toggle fullscreen; use Ctrl+Enter for multiline input.
- Avoid UTF-8 BOM in config files; use `hermes config edit`, VS Code, or a proper editor.
- Native Windows paths differ from macOS/Linux paths. Update configs accordingly.
- Some examples from Linux docs may need PowerShell equivalents.
- If Python/socket/sandbox errors occur, check Windows env vars such as SYSTEMROOT/WINDIR/COMSPEC.

---

## Do Not Do

- Do not push Ubuntu Server/Proxmox unless Neima reopens that choice.
- Do not make WSL the main Hermes environment unless explicitly requested.
- Do not blindly copy Mac `.hermes` over Windows `.hermes`.
- Do not restore Home Assistant before Windows/Hermes/Docker/Ray/Ollama basics are stable.
- Do not expose RDP or services directly to the internet; use Tailscale/local LAN.
- Do not scatter canonical files between OneDrive, Desktop, Downloads, WSL, and random Docker volumes.
- Do not make Ollama the only/default Hermes model early; use it as a local lane/profile.

---

## Useful User/Environment Facts

- User name: Neima.
- Ned repo on Mac was `/Users/neimaseirafi/Documents/ned` and remote is `https://github.com/neimaseirafihtx/ned.git`.
- On Windows, canonical Ned path should become `C:\Users\<user>\Documents\ned`.
- Neima's Git commit identity email: `neime.seirafi@gmail.com`.
- Neima prefers proactive/scheduled Hermes messages in the main Telegram DM only, not Ned group.
- Neima wants Ned/Hermes to act as AI/IT infrastructure coach.
- Neima's near-term priority: Ned/HA/Ray/local-AI concurrency, expandability, internal storage, and verified backups.
- Home Assistant write/control actions should remain approval-gated; light control is okay; Sonos/TV changes off-limits for now.

---

## First Thing to Ask/Do in Future Session

If Neima says the PowerSpec is ready, ask/prompt him to run these in PowerShell and paste output:

```powershell
hostname
Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion, CsManufacturer, CsModel, CsTotalPhysicalMemory
Get-NetAdapter
nvidia-smi
```

Then proceed phase by phase. Keep the user from turning it into a marathon. The goal is one verified phase at a time.
