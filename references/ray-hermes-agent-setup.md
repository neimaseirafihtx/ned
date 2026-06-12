# Ray Hermes Agent Setup Notes

Generated: 2026-06-03 21:05:19 CDT

Purpose: temporary handoff documentation to later move into the Ned repo when permissions are restored.

Secrets policy: no raw tokens, OAuth codes, bot tokens, or credentials are included here. Any credential value is recorded as [REDACTED].

## Summary

We set up a Docker-isolated Hermes agent for Ray, connected it to Ray's own Telegram bot, verified Telegram access, verified OneDrive-backed file exchange through `/shared`, recovered after Docker Desktop reset/wiped internal Docker objects, and then slimmed the Ray Docker image.

Ray's agent is separate from Neima/Ned's main Hermes setup. It has its own Docker container, Hermes home, Telegram bot, OpenAI/Codex OAuth, and OneDrive-backed shared folder.

## Current Windows Runtime State — 2026-06-11

Ray's Hermes instance now runs on NEIMA_SERVER / PowerSpec Windows under Docker Desktop.

Current host paths:

```text
C:/hermes-friends/ray/compose
C:/hermes-friends/ray/compose/Dockerfile
C:/hermes-friends/ray/compose/docker-compose.yml
C:/hermes-friends/ray/compose/OPERATIONS.md
C:/hermes-friends/ray/hermes-home
C:/hermes-friends/ray/hermes-home/config.yaml
C:/hermes-friends/ray/hermes-home/.env
C:/hermes-friends/ray/workspace
C:/Users/neima/OneDrive/Ray Dropbox
```

Current Docker mounts:

```text
C:/hermes-friends/ray/hermes-home -> /home/hermes/hermes-data
C:/hermes-friends/ray/workspace -> /workspace
C:/Users/neima/OneDrive/Ray Dropbox -> /shared
```

Current API/Desktop exposure:

```text
Host Tailscale bind: 100.120.157.4:8643 -> container 8642/tcp
Health URL: http://100.120.157.4:8643/health
Model name: ray-hermes
```

The API server requires `API_SERVER_KEY` from Ray's private `.env`; do not print or commit the key.

Current Ray Telegram platform toolsets, after cleanup:

```text
clarify
code_execution
cronjob
file
skills
terminal
todo
web
```

`cronjob` is intentionally enabled because Ray should be able to create/manage scheduled jobs from Telegram. `kanban` was intentionally removed because Ray is not currently participating in Hermes Kanban workflows.

Ray's container currently uses:

```text
approvals.mode = off
approvals.cron_mode = deny
```

This is acceptable for Ray only because Docker provides a hard filesystem boundary and the container does not mount Neima's home, Ned repo, SSH keys, Home Assistant credentials, or Docker socket. Do not treat this as a generic default for less-isolated agents.

The Ray Dockerfile remains intentionally unpinned for now: it installs Hermes via the current upstream installer so rebuilds pick up current fixes. Because the image is unpinned, every rebuild/update must be followed by backup, config migration/checks, gateway verification, Telegram pairing verification, cron verification, Tailscale API port verification, authenticated `/v1/models`, and a model smoke test. If Ray becomes mission-critical or unpinned updates cause instability, pin Hermes to a known-good tag/commit and document the bump process.

## Ray Agent Identity

- Container name: `ray-hermes`
- Docker image: `ray-hermes:latest`
- Telegram bot username: `@Trismegis_bot`
- Telegram bot URL: `https://t.me/Trismegis_bot`
- Telegram bot display name seen from BotFather/test: `Hermes Trismegistus`
- Telegram bot token: `[REDACTED]`
- Approved Telegram user:
  - Name: Ray Fitzgerald
  - Telegram user ID: `8614345033`
- Pairing code used during setup: not retained; pairing is already approved.

## Host Paths

Base folder:

```text
/Users/neimaseirafi/hermes-friends/ray
```

Important files/folders:

```text
/Users/neimaseirafi/hermes-friends/ray/compose/docker-compose.yml
/Users/neimaseirafi/hermes-friends/ray/compose/Dockerfile
/Users/neimaseirafi/hermes-friends/ray/hermes-home
/Users/neimaseirafi/hermes-friends/ray/hermes-home/config.yaml
/Users/neimaseirafi/hermes-friends/ray/hermes-home/.env
/Users/neimaseirafi/hermes-friends/ray/hermes-home/auth.json
/Users/neimaseirafi/hermes-friends/ray/workspace
/Users/neimaseirafi/Library/CloudStorage/OneDrive-Personal/Ray Dropbox
```

OneDrive-backed shared folder:

```text
/Users/neimaseirafi/Library/CloudStorage/OneDrive-Personal/Ray Dropbox
```

Inside Ray's container this is mounted as:

```text
/shared
```

## Container Mounts

The compose file maps:

```text
/Users/neimaseirafi/hermes-friends/ray/hermes-home -> /home/hermes/hermes-data
/Users/neimaseirafi/hermes-friends/ray/workspace -> /workspace
/Users/neimaseirafi/Library/CloudStorage/OneDrive-Personal/Ray Dropbox -> /shared
```

Runtime environment includes:

```text
HERMES_HOME=/home/hermes/hermes-data
PYTHONUNBUFFERED=1
```

Resource limits:

```text
mem_limit: 1g
cpus: "2.0"
security_opt: no-new-privileges:true
restart: unless-stopped
```

## Docker Compose

Working directory for compose commands:

```text
/Users/neimaseirafi/hermes-friends/ray/compose
```

Common commands:

```bash
cd /Users/neimaseirafi/hermes-friends/ray/compose
docker compose ps
docker compose up -d
docker compose up -d --force-recreate
docker compose build
docker compose build --no-cache
```

Inspect logs/status:

```bash
docker exec ray-hermes hermes gateway status
docker exec ray-hermes hermes pairing list
docker logs ray-hermes --tail 100
```

Check mounts from inside container:

```bash
docker exec ray-hermes bash -lc 'for p in /shared /workspace "$HERMES_HOME"; do test -d "$p" && echo "OK $p" || echo "MISSING $p"; done'
```

Check memory:

```bash
docker stats --no-stream --format 'table {{.Name}}\t{{.MemUsage}}\t{{.MemPerc}}\t{{.CPUPerc}}' ray-hermes
```

## Telegram Setup

Ray created a new Telegram bot with BotFather:

```text
@Trismegis_bot
```

The bot token was stored in Ray's isolated Hermes home `.env` file and must remain secret:

```text
/Users/neimaseirafi/hermes-friends/ray/hermes-home/.env
```

Do not copy the token into docs, Git, or chat summaries.

Telegram response mode was set to standalone messages:

```text
TELEGRAM_REPLY_TO_MODE=off
```

Ray first messaged the bot and got a pairing prompt:

```text
Hi~ I don't recognize you yet!
Here's your pairing code: [REDACTED]
Ask the bot owner to run:
hermes pairing approve telegram [REDACTED]
```

The pairing was approved in the container with:

```bash
docker exec ray-hermes hermes pairing approve telegram [REDACTED]
```

After approval, `hermes pairing list` showed:

```text
Approved Users (1):
Platform     User ID              Name
telegram     8614345033           Ray Fitzgerald
```

## Tailscale / Hermes Desktop Remote Access

Ray's Docker-isolated Hermes agent can also be accessed by Hermes Desktop over the Mac mini's Tailscale IP via the Hermes API server.

Current non-secret connection details:

```text
Remote URL: http://100.120.157.4:8643
Model name: ray-hermes
Container port: 8642
Host bind: 100.120.157.4:8643 -> 8642/tcp
```

Security posture:

- The Docker port is bound only to the Windows host's Tailscale IP, not `0.0.0.0` on the LAN or public internet.
- Ray must be connected to the Tailscale tailnet / have access to the Windows host.
- `API_SERVER_KEY` is required and stored only in Ray's isolated `.env`; do not commit or print it.
- A one-off connection-instructions file with the token may be placed in Ray's OneDrive outbox when Ray needs to configure Desktop; treat it as a credential.

Host-side compose config includes an `env_file` pointing at Ray's isolated Hermes `.env` and a port mapping for the Tailscale-only API server.

Ray `.env` API-server variables:

```text
API_SERVER_ENABLED=true
API_SERVER_HOST=0.0.0.0
API_SERVER_PORT=8642
API_SERVER_MODEL_NAME=ray-hermes
API_SERVER_KEY=[REDACTED]
```

Verification commands:

```bash
curl http://100.120.157.4:8643/health
# Expected: {"status":"ok","platform":"hermes-agent"}

# Use API_SERVER_KEY from Ray's .env, without printing it:
python - <<'PY'
import urllib.request
from pathlib import Path
key = None
for line in Path('C:/hermes-friends/ray/hermes-home/.env').read_text().splitlines():
    if line.startswith('API_SERVER_KEY='):
        key = line.split('=', 1)[1].strip().strip('"').strip("'")
        break
assert key, 'API_SERVER_KEY missing'
req = urllib.request.Request('http://100.120.157.4:8643/v1/models', headers={'Authorization': 'Bearer ' + key})
print(urllib.request.urlopen(req, timeout=10).read().decode())
PY
# Expected model id: ray-hermes
```

Known Docker Desktop regression: Compose can still declare `100.120.157.4:8643:8642` while Docker's effective port publication disappears (`docker port ray-hermes` empty, `.NetworkSettings.Ports` shows `{"8642/tcp":[]}`). In that case the gateway may be healthy internally but Hermes Desktop/API over Tailscale fails. Recovery is:

```bash
cd /c/hermes-friends/ray/compose
docker compose up -d --force-recreate ray-hermes
docker port ray-hermes
curl -fsS http://100.120.157.4:8643/health
```

## Verified Telegram Functionality

Ray tested Telegram by asking whether the agent could see `/shared` and `/workspace`.

Ray's agent replied that both were accessible:

```text
/shared: accessible
/workspace: accessible
```

The agent saw examples including:

```text
/shared/inbox/test.txt
/shared/outbox/test-summary-from-hermes.md
/workspace/README.md
/workspace/AGENTS.md
```

This verified:

1. Ray can talk to `@Trismegis_bot`.
2. `@Trismegis_bot` is connected to the isolated `ray-hermes` container.
3. Ray is approved as a Telegram user.
4. Ray's agent can access `/shared` and `/workspace`.
5. `/shared` maps back to the OneDrive-backed Ray Dropbox folder on the Mac.

## OneDrive / File Flow

Earlier smoke test verified Ray's Hermes agent could:

- access `/workspace`
- access `/shared`
- read `/shared/inbox/test.txt`
- write `/shared/outbox/test-summary-from-hermes.md`

Host-side expected output path:

```text
/Users/neimaseirafi/Library/CloudStorage/OneDrive-Personal/Ray Dropbox/outbox/test-summary-from-hermes.md
```

Recommended Ray workflow:

1. Ray drops files into OneDrive folder:

```text
Ray Dropbox/inbox/
```

2. Ray messages `@Trismegis_bot`, e.g.:

```text
Please read the newest file in /shared/inbox, summarize it, and write the summary to /shared/outbox/telegram-summary.md. Do not modify files in /shared/inbox.
```

3. Hermes writes results to:

```text
/shared/outbox
```

4. Neima/Ray can see those results in OneDrive:

```text
Ray Dropbox/outbox/
```

## Docker Desktop Reset Incident and Recovery

Neima changed Docker Desktop settings to roughly:

```text
2GB RAM
1GB swap
40GB disk
```

Docker showed a warning with a red `resize anyway` option. After clicking it, Docker's internal Linux disk image appeared to reset/wipe Docker-managed objects:

- containers were gone
- images were gone
- build cache was gone

Important: Ray's durable data survived because it was bind-mounted from the Mac host, not stored inside Docker-managed volumes/images.

Surviving host data included:

```text
/Users/neimaseirafi/hermes-friends/ray/hermes-home
/Users/neimaseirafi/hermes-friends/ray/workspace
/Users/neimaseirafi/Library/CloudStorage/OneDrive-Personal/Ray Dropbox
```

Recovery steps performed:

```bash
cd /Users/neimaseirafi/hermes-friends/ray/compose
docker compose build
docker compose up -d
```

After recovery, verified:

- Docker reachable
- `ray-hermes` recreated and running
- gateway running as PID 1
- Telegram polling connected
- Ray still approved
- `/shared`, `/workspace`, and `$HERMES_HOME` mounted

## Docker Slimming / Cleanup

The first rebuild after Docker reset produced a large image and cache because the default Hermes install created a general-purpose desktop-capable stack:

Observed bloat sources:

- Playwright browser binaries / Chromium cache
- Node.js
- npm cache
- node_modules
- Electron cache
- node-gyp cache
- uv/Python package cache
- Hermes repo `.git`
- Hermes tests and website/app desktop assets
- Debian build tools

Observed before slimming:

```text
ray-hermes image: around 11.57GB
build cache: around 6.79GB
total Docker usage: roughly 18GB+
```

Dockerfile was patched to install Hermes with:

```bash
--skip-browser
```

Then remove unnecessary runtime paths:

```text
$HERMES_HOME/node
$HERMES_HOME/hermes-agent/.git
$HERMES_HOME/hermes-agent/node_modules
$HERMES_HOME/hermes-agent/apps
$HERMES_HOME/hermes-agent/website
$HERMES_HOME/hermes-agent/tests
$HOME/.cache
$HOME/.npm
$HOME/.local/bin/node
$HOME/.local/bin/npm
$HOME/.local/bin/npx
```

`build-essential` was removed from apt dependencies.

`xz-utils` was added because Hermes installer needs it to unpack Node during installation even though Node is deleted after install.

After slimming, rebuilt with:

```bash
cd /Users/neimaseirafi/hermes-friends/ray/compose
docker compose build --no-cache
docker compose up -d --force-recreate
```

Then pruned safe build cache:

```bash
docker builder prune -f
docker image prune -f
```

Post-cleanup verification:

```text
ray-hermes: running
Hermes gateway: running
Telegram: connected polling mode
Approved user: Ray Fitzgerald / 8614345033
/shared: OK
/workspace: OK
/home/hermes/hermes-data: OK
```

Post-cleanup sizes:

```text
docker images ray-hermes: 893MB
Docker system df images: 1.497GB
Build cache: 894MB, 0B reclaimable
Container writable layer: 72.5MB
```

Post-cleanup memory:

```text
ray-hermes: ~142.9MiB / 1GiB
about 14%
```

## Intentional Tradeoff

Browser automation inside Ray's container is intentionally removed.

This is acceptable because Ray's current intended use is:

- Telegram chat
- file handoff through OneDrive `/shared`
- terminal/file/code/web basics
- Hermes skills
- writing outputs to `/shared/outbox`

If Ray later needs browser automation, options are:

1. re-enable browser tooling in this image, or
2. create a separate heavier browser-capable Ray agent/container.

## Security / Isolation Notes

Ray Hermes should remain isolated from Neima/Ned's main host and tools.

Current security posture:

- Separate Docker container: `ray-hermes`
- Separate Hermes home: `/Users/neimaseirafi/hermes-friends/ray/hermes-home`
- Separate Telegram bot: `@Trismegis_bot`
- Separate OneDrive file handoff folder
- No Home Assistant access
- No SSH access
- No host `~/.hermes` exposure
- No Neima/Ned Telegram bot reuse
- Secrets are local in Ray's Hermes home and not documented

Ray's agent can see and write within the bind-mounted paths:

```text
/shared
/workspace
/home/hermes/hermes-data
```

Do not mount Neima's personal home, Ned repo, Home Assistant token files, SSH keys, or the default `~/.hermes` into Ray's container unless explicitly decided later.

## Ray Handoff Package Prompt

Ray is expected to use Claude to create handoff `.md` packages and upload supporting files such as Excel plans into `/shared/inbox`.

Recommended first message Ray can send to Hermes after uploading files:

```text
Please read /shared/inbox/ray-hermes-handoff.md, inspect the referenced files in /shared/inbox, and complete the requested task breakdown. Start by writing /shared/outbox/file-inventory.md and /shared/outbox/execution-plan.md, then proceed with the remaining deliverables. Do not modify files in /shared/inbox.
```

Recommended output folder:

```text
/shared/outbox
```

## Operational Checklist

To verify Ray is healthy:

```bash
cd /Users/neimaseirafi/hermes-friends/ray/compose
docker compose ps
docker exec ray-hermes hermes gateway status
docker exec ray-hermes hermes pairing list
docker stats --no-stream --format 'table {{.Name}}\t{{.MemUsage}}\t{{.MemPerc}}\t{{.CPUPerc}}' ray-hermes
docker exec ray-hermes bash -lc 'for p in /shared /workspace "$HERMES_HOME"; do test -d "$p" && echo "OK $p" || echo "MISSING $p"; done'
```

Expected healthy signs:

```text
ray-hermes Up
Gateway is running
telegram connected in logs
Ray Fitzgerald approved
OK /shared
OK /workspace
OK /home/hermes/hermes-data
memory usually under 250MiB idle
```

## Files To Later Move Into Ned Repo

This file itself should be moved into the Ned repo when permissions are restored. Suggested path:

```text
/Users/neimaseirafi/Documents/ned/references/ray-hermes-agent-setup.md
```

Optionally split into:

```text
/Users/neimaseirafi/Documents/ned/references/ray-hermes-agent-setup.md
/Users/neimaseirafi/Documents/ned/operations/ray-hermes-runbook.md
```

Do not include raw token values in Git.
