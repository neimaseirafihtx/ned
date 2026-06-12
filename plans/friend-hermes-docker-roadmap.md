# Friend Hermes Docker Roadmap

## Goal

Add a safe, low-friction path for hosting a separate Hermes Agent instance for a friend while keeping Neima's Ned/Hermes, Home Assistant, credentials, and personal files isolated.

This is a roadmap item, not an active build. Do not implement until Neima explicitly says to proceed.

## Current Decision

- Host first experiment on the Mac Mini rather than buying/building a separate Windows/Linux server now.
- Use Docker, not a VM, for the first friend-hosted Hermes environment.
- Use OpenAI OAuth / OpenAI Codex-style auth for the friend rather than Neima's API keys.
- Keep friend Hermes isolated from Neima's `~/.hermes`, Ned repo, Home Assistant token, SSH keys, and Mac home folder.
- Re-evaluate hardware only after a real pilot shows memory/CPU pressure.

## Why This Comes After Current Phase 3 Work

This belongs in the AI Track's Multi-Agent & Autonomous Systems direction, but it should not displace the current Phase 3 priorities:

1. Keep Home Assistant useful and safe.
2. Build the custom Ned MCP server.
3. Keep the daily health brief / cron lane stable.
4. Then pilot one friend Hermes Docker container.

## Proposed Host Architecture

Initial host:

```text
Mac Mini M4 16GB
  macOS Tahoe
  Docker Desktop
    friend-hermes-<name> container
      /home/hermes/.hermes   # friend-owned Hermes home volume
      /workspace             # friend-owned sandbox workspace
```

Potential future host if needed:

```text
Dedicated mini PC / Proxmox host
  Home Assistant OS VM
  Docker VM/LXC
    friend Hermes containers
```

Do not buy/build a separate server only for this until a pilot proves the Mac Mini is not enough.

## Container Isolation Rules

Each friend gets a separate Docker Compose project with:

- dedicated `hermes-home/` volume
- dedicated `workspace/` volume
- dedicated `.env` file for non-Hermes platform secrets, if any
- their own OpenAI OAuth token stored in their Hermes auth state
- their own Telegram/Discord bot token if gateway is used
- explicit CPU/RAM limits

Never mount:

- `/Users/neimaseirafi`
- Neima's `~/.hermes`
- the Ned repo, unless a read-only copy is intentionally shared later
- Home Assistant token/config
- SSH keys
- host Docker socket (`/var/run/docker.sock`)
- browser profiles or logged-in app data

## Suggested Folder Layout

Use external storage if available and stable; otherwise start under a clearly named local server directory.

```text
/Volumes/Mac External/hermes-friends/
  template/
    Dockerfile
    docker-compose.yml
    README.md
    .env.example
  friend-name/
    docker-compose.yml
    hermes-home/
    workspace/
    .env
```

If the Samsung T9 is not mounted reliably at boot, use an internal path first and move later.

## Initial Resource Limits

For a basic OpenAI-backed Hermes chat/gateway container:

- 1-2 CPU cores
- 1-2GB RAM
- small workspace quota by convention

For coding/browser-heavy usage:

- 2-4 CPU cores
- 3-4GB RAM
- enable only after the basic container is stable

Mac Mini 16GB constraint: start with one friend only. Do not host several friend containers while HAOS, Docker, Ollama, and Ned gateway are all active until memory pressure is measured.

## Tool Policy

Start restricted:

- web/search if needed
- memory/session state inside the friend's profile only
- file access only inside `/workspace`
- no Home Assistant toolset
- no host terminal access outside the container
- no messaging except their own gateway bot/channel
- no cron jobs until basic trust and isolation are proven

Add more tools only after reviewing risk.

## OpenAI OAuth Onboarding Flow

Planned flow:

1. Create friend directory from template.
2. Start container interactively.
3. Run Hermes setup/auth inside the container.
4. Friend completes OpenAI OAuth/device-code flow with their own account.
5. Verify with `hermes auth list` inside the container.
6. Set the model/provider for that container/profile.
7. Test one CLI prompt.
8. Only then configure gateway, if needed.

OAuth token must remain inside that friend's mounted `hermes-home/` and must not be copied into Neima's profile.

## Verification Checklist Before Launch

- `docker compose config` passes.
- Container starts without privileged mode.
- Container cannot see `/Users/neimaseirafi`.
- Container cannot see Neima's `~/.hermes`.
- Container cannot access host Docker socket.
- Hermes runs a test prompt using the friend's auth.
- File writes land only in the friend's `workspace/`.
- Gateway, if enabled, uses the friend's bot/channel, not Neima's Ned Telegram group.
- Mac Mini memory pressure remains acceptable after 24-48 hours.

## Deferral Criteria

Pause or move to a dedicated host if any of these happen:

- Mac Mini memory pressure becomes consistently high.
- HAOS/UTM stability regresses.
- Docker Desktop becomes a boot/restart reliability problem.
- Friend use requires broad terminal access or risky tools.
- More than one or two friends need persistent agents.
- Neima upgrades the Mac Mini and wants to re-baseline the architecture.

## Future Hardware Note

A separate mini PC with Proxmox is attractive for Home Assistant + Docker isolation, but it also duplicates much of the Mac Mini's reason to exist. Current preference is to preserve the Mac Mini as the Ned/home-infra hub and only add hardware when there is a proven operational need.

---

## Current State (2026-06-11)

Ray's container is live on the Windows server (`Neima_Server`), not the Mac Mini (decommissioned 2026-06-09).

**Container:**
```
IMAGE               COMMAND                CONTAINER NAME
ray-hermes:latest   "hermes gateway run"   ray-hermes
```

**Shell access:**
```powershell
docker exec -it ray-hermes /bin/bash
```

If bash isn't available:
```powershell
docker exec -it ray-hermes /bin/sh
```

Files live at `C:\hermes-friends\ray\` on the Windows server.
