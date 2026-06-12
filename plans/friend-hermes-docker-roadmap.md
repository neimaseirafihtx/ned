# Friend Hermes Docker — Ray's Container

## Current State (2026-06-11)

Ray's Hermes instance is **live** on the Windows server (`Neima_Server`). The Mac Mini architecture in earlier versions of this doc is historical — the Mac Mini was decommissioned 2026-06-09.

**Container:**
```
IMAGE               COMMAND                CONTAINER NAME
ray-hermes:latest   "hermes gateway run"   ray-hermes
```

**Files:** `C:\hermes-friends\ray\` on `Neima_Server`

**Bot:** `@Trismegis_bot` (Ray's own Telegram bot, not Ned's)

**Auth:** Ray's own OpenAI OAuth — no shared keys with Neima

---

## Shell Access

```powershell
docker exec -it ray-hermes /bin/bash
```

If bash isn't in the image:
```powershell
docker exec -it ray-hermes /bin/sh
```

---

## Host Architecture

```text
Neima_Server (Windows 11 Pro)
  Docker Desktop (WSL2 backend)
    ray-hermes container
      hermes-home/   # Ray's Hermes profile (isolated volume)
      workspace/     # Ray's sandbox workspace (isolated volume)
```

---

## Isolation Rules

Ray's container is fully isolated from Neima's stack. Never mount or share:

- `C:\Users\neima\` or any subfolder
- Neima's `%APPDATA%\Local\hermes\` (Hermes home)
- The Ned repo (`C:\Users\neima\Documents\ned`)
- Home Assistant token or config
- Neima's SSH keys
- Host Docker socket (`\\.\pipe\docker_engine`)
- Neima's Telegram bot or Ned group

Each friend gets:
- Dedicated Docker Compose project under `C:\hermes-friends\<name>\`
- Dedicated `hermes-home/` volume
- Dedicated `workspace/` volume
- Dedicated `.env` file for their own secrets
- Their own OpenAI OAuth token stored inside their Hermes profile
- Their own Telegram/Discord bot token
- Explicit CPU/RAM limits

---

## Resource Limits

For a basic OpenAI-backed Hermes chat/gateway container:
- 1-2 CPU cores
- 1-2 GB RAM

For coding/browser-heavy usage:
- 2-4 CPU cores
- 3-4 GB RAM (monitor against Ollama + Hermes pressure on 32 GB total)

---

## Tool Policy

Start restricted:
- Web/search if needed
- Memory/session state inside the friend's profile only
- File access only inside `/workspace`
- No Home Assistant toolset
- No host terminal access outside the container
- No messaging except their own gateway bot/channel
- No cron jobs until basic trust and isolation are proven

Add tools only after reviewing risk.

---

## Adding a New Friend

1. Copy `C:\hermes-friends\template\` → `C:\hermes-friends\<name>\`
2. Set resource limits and `.env` in the new directory
3. Start container interactively: `docker compose up`
4. Run Hermes setup/auth inside the container: `docker exec -it <container> hermes auth login`
5. Friend completes OpenAI OAuth with their own account
6. Verify: `docker exec -it <container> hermes auth list`
7. Set model/provider for that container
8. Test one CLI prompt
9. Only then configure gateway (Telegram bot token, etc.)

OAuth token must stay inside the friend's mounted `hermes-home/` — never copy into Neima's profile.

---

## Verification Checklist Before Adding New Friends

- `docker compose config` passes
- Container starts without privileged mode
- Container cannot see `C:\Users\neima\`
- Container cannot see Neima's Hermes home
- Container cannot access host Docker socket
- Hermes runs a test prompt using the friend's auth
- File writes land only in the friend's `workspace/`
- Gateway uses the friend's bot/channel, not Ned's Telegram group
- Memory pressure on `Neima_Server` remains acceptable after 24-48 hours

---

## Future Friends

No new hardware planned just for this. The Windows server (32 GB RAM) has headroom for a couple of isolated containers alongside Hermes, Ollama, and Docker. Reassess if more than two or three friends need persistent agents simultaneously.
