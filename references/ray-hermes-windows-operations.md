# Ray Hermes Windows Operations Runbook

This is the current operational runbook for Ray's Docker-isolated Hermes instance on NEIMA_SERVER / PowerSpec Windows.

Secrets policy: this file intentionally does not include raw bot tokens, API keys, OAuth tokens, bearer tokens, or connection-instruction files containing credentials.

## Runtime shape

Container:

```text
ray-hermes
```

Important host paths:

```text
C:/hermes-friends/ray/compose
C:/hermes-friends/ray/compose/Dockerfile
C:/hermes-friends/ray/compose/docker-compose.yml
C:/hermes-friends/ray/compose/OPERATIONS.md
C:/hermes-friends/ray/hermes-home  -> /home/hermes/hermes-data
C:/hermes-friends/ray/workspace    -> /workspace
C:/Users/neima/OneDrive/Ray Dropbox -> /shared
```

API/Desktop exposure:

```text
100.120.157.4:8643 -> container 8642/tcp
health: http://100.120.157.4:8643/health
model: ray-hermes
```

The API server requires `API_SERVER_KEY` from Ray's private `hermes-home/.env`. Do not print or commit that key.

## Known Docker Desktop port-publication failure

Observed failure mode after Docker Desktop/container restarts:

- `docker-compose.yml` still declares `100.120.157.4:8643:8642`.
- Ray Hermes is healthy inside the container.
- `docker exec ray-hermes ...` works.
- But Docker's effective port publication is missing:

```bash
docker port ray-hermes
# no output

docker inspect ray-hermes --format '{{json .NetworkSettings.Ports}}'
# {"8642/tcp":[]}
```

Impact:

- Ray Telegram/gateway may still work.
- Hermes Desktop/API over Tailscale fails.
- `curl http://100.120.157.4:8643/health` fails.

Recovery, when Ray is not actively using the agent:

```bash
cd /c/hermes-friends/ray/compose
docker compose up -d --force-recreate ray-hermes
```

Verify after recovery:

```bash
docker ps --filter name=ray-hermes --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
docker port ray-hermes
curl -fsS http://100.120.157.4:8643/health
docker exec ray-hermes hermes gateway status
docker exec ray-hermes hermes pairing list
```

Expected good signs:

```text
100.120.157.4:8643->8642/tcp
8642/tcp -> 100.120.157.4:8643
{"status": "ok", "platform": "hermes-agent", "version": "..."}
✓ Gateway is running
Ray Fitzgerald approved
```

## Host watchdog

Ned's main Hermes profile has a host-side script-only cron job:

```text
Name: Ray Hermes Docker watchdog
Script: ray-hermes-watchdog.py
Schedule: every 30m
Delivery: telegram
Behavior: quiet when all green; sends an alert only on WARN/FAIL
```

Script path on host:

```text
C:/Users/neima/AppData/Local/hermes/scripts/ray-hermes-watchdog.py
```

Manual full report:

```bash
python C:/Users/neima/AppData/Local/hermes/scripts/ray-hermes-watchdog.py --always
```

Manual quiet watchdog mode:

```bash
python C:/Users/neima/AppData/Local/hermes/scripts/ray-hermes-watchdog.py
```

Empty stdout in quiet mode means all green. The cron job uses the Python script rather than a `.sh` script because no-agent cron on this Windows host previously mangled native paths when invoking `.sh` scripts through bash.

## Ray Telegram cron permissions

Ray is intentionally allowed to create/manage Hermes cron jobs from Telegram. Keep `cronjob` enabled in Ray's Telegram platform toolsets unless Neima explicitly revokes that capability.

Current desired Telegram platform toolsets:

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

`kanban` was intentionally removed from Ray's Telegram platform toolsets because Ray is not currently participating in Hermes Kanban workflows.

## Approval mode note

Ray's isolated container currently uses:

```text
approvals.mode = off
approvals.cron_mode = deny
```

That is acceptable for Ray only because the container has a hard Docker filesystem boundary and does not mount Neima's home, Ned repo, SSH keys, Home Assistant credentials, or the Docker socket. Do not generalize this as a default posture for broader or less-isolated agents. Main Ned can have different approval settings when Neima explicitly chooses admin-speed over prompts, but Ray's setting is justified by container isolation, not by trust alone.

## Dockerfile version-pinning decision

The Ray Dockerfile intentionally installs Hermes from the current upstream installer instead of pinning a specific release/commit. Decision for now: leave it unpinned.

Reason:

- Ray is still in an active/evolving setup phase.
- Rebuilds can pick up current Hermes fixes without manual Dockerfile edits.
- Durable state is bind-mounted outside the image and backed up before updates.

Operational rule: every rebuild/update must be followed by config migration/checks and live verification of gateway, Telegram pairing, cron jobs, Tailscale API port publication, authenticated `/v1/models`, and a model smoke test. If Ray's setup becomes mission-critical or updates start causing instability, pin Hermes in the Dockerfile to a known-good tag/commit and document the bump process here.

## Update procedure

Before rebuilding/updating Ray's image, create a coherent backup of the bind-mounted state. The safest path is to stop the container briefly before archiving `hermes-home`:

```bash
TS=$(date -u +%Y%m%dT%H%M%SZ)
BACKUP_DIR="/c/hermes-friends/ray/backups/update-$TS"
mkdir -p "$BACKUP_DIR"
docker stop ray-hermes
tar --warning=no-file-changed -czf "$BACKUP_DIR/ray-hermes-home.tgz" -C /c/hermes-friends/ray hermes-home
tar -czf "$BACKUP_DIR/ray-compose-workspace.tgz" -C /c/hermes-friends/ray compose workspace
(cd "$BACKUP_DIR" && sha256sum *.tgz > SHA256SUMS.txt && sha256sum -c SHA256SUMS.txt)
```

Then rebuild/recreate and migrate config:

```bash
cd /c/hermes-friends/ray/compose
docker compose build --pull --no-cache ray-hermes
docker compose up -d --force-recreate ray-hermes
docker exec ray-hermes hermes config migrate
docker restart ray-hermes
```

Post-update verification:

```bash
docker exec ray-hermes hermes --version
docker exec ray-hermes hermes config check
docker exec ray-hermes hermes gateway status
docker exec ray-hermes hermes pairing list
docker exec ray-hermes hermes cron list --all
docker port ray-hermes
curl -fsS http://100.120.157.4:8643/health
python C:/Users/neima/AppData/Local/hermes/scripts/ray-hermes-watchdog.py --always
docker exec ray-hermes hermes chat -q 'Health check: reply with exactly OK_RAY_HERMES.' --toolsets safe -Q
```

Latest verified update, 2026-06-11:

```text
Hermes Agent: v0.16.0, reported Up to date
Config migrated: v26 -> v29
Gateway: running
Pairing: Ray Fitzgerald approved
Cron jobs: 3 active AT100 jobs survived
Telegram toolsets: cronjob present, kanban removed
Tailscale API port: 100.120.157.4:8643 -> 8642/tcp
Authenticated /v1/models: ray-hermes
Smoke test: OK_RAY_UPDATED / OK_RAY_NO_KANBAN
Host watchdog: green
```

## Security boundaries to preserve

Do not mount these into Ray's container:

```text
C:/Users/neima
C:/Users/neima/AppData/Local/hermes or C:/Users/neima/.hermes
C:/Users/neima/Documents/ned
C:/Users/neima/.ssh
Docker socket
Home Assistant credentials
broad OneDrive root
```

Only mount Ray's private Hermes home, Ray workspace, and the narrow Ray Dropbox shared folder.
