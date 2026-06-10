# Ray Claude Code — Execution Roadmap

*Created 2026-06-09. Goal: add a Claude Code instance to Ray's server presence on the Windows server, remotely drivable from Ray's phone via Claude Code Remote Control, with access to the Ray Dropbox (OneDrive, synced locally).*

---

## 1. Goal

Expand Ray's footprint on `Neima_Server` from "Hermes in Docker" to "Hermes + Claude Code in Docker":

1. A Claude Code instance runs in a terminal context inside Ray's isolated container environment.
2. Ray connects to it from his phone using Claude Code **Remote Control** (Claude mobile app → session list → his session).
3. The instance has read/write access to the Ray Dropbox at `C:\Users\neima\OneDrive\Ray Dropbox` (already synced locally and pinned "Always keep on this device").

Same isolation philosophy as the Hermes pilot: Ray's own accounts, Ray's own volumes, zero access to Neima's Hermes, HA, SSH keys, or home folder.

---

## 2. Current container assessment (2026-06-09)

Inspected `ray-hermes` container + `C:\hermes-friends\ray\compose\{Dockerfile,docker-compose.yml}`.

| Aspect | Current state | Verdict for this project |
|---|---|---|
| Base image | `python:3.11-slim` (Debian), non-root `hermes` user | ✅ Fine. Claude Code native binary runs on glibc Debian; no Node needed (native installer, not npm) |
| Node/npm | Deliberately stripped from image | ✅ Not a blocker — Claude Code's native installer doesn't require Node |
| Mounts | `workspace → /workspace`, `hermes-home → /home/hermes/hermes-data`, `OneDrive Ray Dropbox → /shared` (RW) | ✅ Dropbox access is already solved — `/shared` is exactly what Claude Code needs |
| OneDrive hydration | Ray Dropbox folder is **pinned** (attribute 0x80000, "Always keep on this device") | ✅ No placeholder/Files-On-Demand risk through the bind mount |
| Network | Outbound open; one inbound port (8643 on Tailscale IP for Hermes gateway) | ✅ Remote Control is **outbound HTTPS only** — no new ports, no firewall work |
| Resources | `mem_limit: 2g`, `cpus: 2.0` | ⚠️ Fine for Hermes alone; Claude Code needs its own headroom (run it as a separate service with its own limits) |
| Restart policy | `unless-stopped` | ✅ Right model — Remote Control exits after ~10 min of network outage, so supervision matters |
| Secrets | `env_file: hermes-home/.env` (Ray's Telegram/OpenAI) injected into the Hermes service | ⚠️ Do **not** reuse this env_file for the Claude Code service — keep Hermes secrets out of Claude's process env |
| Claude credential persistence | None — `~/.claude` would die on container recreate | ❌ Needs a new persistent volume (use `CLAUDE_CONFIG_DIR`) |

**Bottom line:** the existing `ray-hermes` service needs **zero changes**. The work is additive: install Claude Code in the shared image and add a second compose service.

---

## 3. Architecture decision

**Run Claude Code as a second service in the same compose project, same image, separate container.**

- Same image: one Dockerfile to maintain; Claude Code binary baked in at build.
- Separate container (`ray-claude`): independent restart/resource limits; a Claude Code crash or rebuild never touches the Hermes gateway, and vice versa.
- Server mode (`claude remote-control`) as the container command: it's designed to run unattended, waits for connections, and serves sessions Ray opens from his phone. No tmux hacks needed.
- Mounts: `/workspace` (shared with Hermes — same project files) and `/shared` (Ray Dropbox). **Not** `hermes-home` — Claude Code has no business in Hermes runtime state, auth.json, or .env.
- Identity: Ray's own claude.ai account, logged in once interactively; credentials persist in a new `claude-config` volume via `CLAUDE_CONFIG_DIR`.

Key Remote Control facts driving this design (verified against [docs](https://code.claude.com/docs/en/remote-control), 2026-06-09):

- Requires Claude Code **v2.1.51+** and a **claude.ai login** (Pro/Max/Team/Enterprise). API keys and `claude setup-token` long-lived tokens are explicitly **not** supported — the one-time login must be the full OAuth `/login` flow.
- **Outbound HTTPS only** — the session registers with the Anthropic API and polls; no inbound ports.
- Server mode supports multiple concurrent sessions (default capacity 32); `--spawn same-dir` (default) is right for a single shared workspace.
- Sessions appear in the Claude mobile app under **Code** with a computer icon + green dot. There's also a session URL + QR code.
- If the machine loses network for ~10+ minutes the process **exits** — `restart: unless-stopped` brings it back automatically (as a fresh session registration).
- Push notifications to Ray's phone work once he's signed into the mobile app with the same account (v2.1.110+, enable "Push when Claude decides" in `/config`).

---

## 4. Proposed config changes

### 4.1 Dockerfile (append before `CMD`)

```dockerfile
# Claude Code — native binary install (no Node required).
# Used by the ray-claude service; harmless in the hermes service.
RUN curl -fsSL https://claude.ai/install.sh | bash

# Container is rebuilt to update; don't let the binary self-update into the ephemeral layer.
ENV DISABLE_AUTOUPDATER=1
```

The installer drops the binary into `~/.local/bin/claude`, which is already on `PATH`. Note the existing cleanup step removes `~/.local/bin/node|npm|npx` — leave that alone, it doesn't touch `claude`.

### 4.2 docker-compose.yml (new service)

```yaml
  ray-claude:
    image: ray-hermes:latest        # same image, built once
    container_name: ray-claude
    restart: unless-stopped
    depends_on: []                  # independent of the hermes gateway
    environment:
      CLAUDE_CONFIG_DIR: /home/hermes/claude-config
      PYTHONUNBUFFERED: "1"
    # NO env_file — Hermes secrets stay out of this container
    working_dir: /workspace
    stdin_open: true
    tty: true
    command: ["claude", "remote-control", "--name", "Ray Claude Code"]
    volumes:
      - "C:/hermes-friends/ray/workspace:/workspace"
      - "C:/Users/neima/OneDrive/Ray Dropbox:/shared"
      - "C:/hermes-friends/ray/claude-config:/home/hermes/claude-config"
    mem_limit: 3g
    cpus: "2.0"
    security_opt:
      - no-new-privileges:true
```

Notes:
- `CLAUDE_CONFIG_DIR` relocates `.claude.json`, credentials, settings, and history into the mounted volume — login and workspace trust survive container recreation.
- `tty: true` keeps server mode's terminal UI happy; `docker attach ray-claude` shows the session URL (and spacebar toggles the QR code).
- No ports section at all.
- Host RAM check: Hermes 2g + Claude 3g + HA VM later (2-4g) on 32GB — fine.

### 4.3 Host-side

- Create `C:\hermes-friends\ray\claude-config\` before first run.
- OneDrive pinning: already done (verified) — no action.

---

## 5. Execution phases

### Phase 0 — Prerequisites (Ray + Neima, ~1 day calendar time)

- [x] **Ray has a claude.ai Pro subscription** (confirmed 2026-06-09) — meets the Remote Control requirement; his account, his billing, same model as his OpenAI OAuth.
- [ ] Ray installs the **Claude mobile app** (iOS/Android) and signs into that account.
- [ ] Confirm Docker Desktop + the Windows server have been stable since migration (gateway survives reboot — still an open verification item from the migration).

### Phase 1 — Image + compose changes (~30 min)

- [ ] Append the Claude Code install block to `C:\hermes-friends\ray\compose\Dockerfile`.
- [ ] Add the `ray-claude` service to `docker-compose.yml` (section 4.2).
- [ ] Create `C:\hermes-friends\ray\claude-config\`.
- [ ] `docker compose build` then verify: `docker run --rm ray-hermes:latest claude --version` → must be ≥ 2.1.51.
- [ ] Recreate the Hermes service from the new image (`docker compose up -d ray-hermes`) and confirm Ray's Hermes still answers on Telegram — same image now, so prove no regression before touching anything else.

### Phase 2 — One-time interactive setup (~20 min, coordinate with Ray)

- [ ] Start the service stopped-ish for setup: `docker compose run --rm -it ray-claude bash`.
- [ ] Run `claude` in `/workspace` → accept the **workspace trust** dialog (required for Remote Control).
- [ ] Run `/login` → choose claude.ai → this prints an OAuth URL + code flow. **Ray completes the browser step on his own device** (send him the URL via his Telegram/Hermes); paste the resulting code back into the terminal. Neima never touches Ray's password.
- [ ] Sanity-check identity: `/status` should show Ray's account, not Neima's.
- [ ] Optional hardening while in the session: set sensible permission defaults (Ray will be approving tool actions from his phone UI).
- [ ] Exit. Credentials now live in `claude-config\` — back this folder's existence into the friend-template checklist later.

### Phase 3 — Remote Control live (~15 min)

- [ ] `docker compose up -d ray-claude`.
- [ ] `docker attach ray-claude` (or `docker logs ray-claude`) → grab the **session URL**; send it to Ray via Telegram.
- [ ] Ray opens the URL (or Claude app → **Code** tab → finds "Ray Claude Code" with green dot) → sends a first prompt from his phone.
- [ ] Verify the prompt executes in the container (watch `docker logs`).
- [ ] Ray enables push: in the session run `/config` → **Push when Claude decides** → ON. Test with "notify me when this finishes" on a short task.

### Phase 4 — Dropbox file-flow validation (~15 min)

- [ ] From Ray's phone: "create a file named `claude-write-test.md` in /shared with today's date" → confirm it appears in `C:\Users\neima\OneDrive\Ray Dropbox` and syncs to OneDrive cloud.
- [ ] Reverse direction: drop a file into the OneDrive folder (Ray's side), have Claude read it from `/shared`.
- [ ] Update `workspace/AGENTS.md` (Claude Code reads it as project context — verify; add a `CLAUDE.md` if needed) documenting: `/shared` = Ray Dropbox conventions, what lives in `/workspace`, what Claude should and shouldn't touch.

### Phase 5 — Ops, monitoring, docs (~1 hr)

- [ ] **Restart drill:** `docker restart ray-claude` → confirm server mode re-registers and the session reappears on Ray's phone (it will be a *new* session entry — set expectation with Ray).
- [ ] **Reboot drill:** confirm both `ray-hermes` and `ray-claude` come up after a Windows reboot (Docker Desktop starts on login — already configured).
- [ ] Add `ray-claude` checks to the planned Windows health-brief rewrite (container up, process alive, recent log line): container state via `docker inspect -f '{{.State.Status}}' ray-claude`.
- [ ] Update `references/ray-hermes-agent-setup.md` + memory (`user_windows_server.md`, roadmap) with the new service.
- [ ] Update cadence: rebuild image monthly-ish or when a Remote Control fix matters (`docker compose build --no-cache ray-claude` picks up latest Claude Code; autoupdater stays disabled).
- [ ] Fold lessons into the **friend Hermes template** roadmap item (Claude Code becomes an optional module of the friend stack).

---

## 6. Risks & gotchas

| Risk | Mitigation |
|---|---|
| Remote Control is a **research preview** — flags/behavior may shift | Pin expectations; rebuild image to pick up fixes; check release notes when something breaks |
| ~10 min network outage kills the process | `restart: unless-stopped`; health check in the daily brief |
| Session entries multiply after restarts (each registration is a new session) | Name the session (`--name "Ray Claude Code"`); tell Ray to pick the one with the green dot |
| Workspace trust or login lost | Both persist in `claude-config` volume; only a volume wipe forces re-login |
| Claude Code and Hermes both writing `/workspace` | Low risk (Ray coordinates himself); AGENTS.md conventions; worst case split a `claude/` subdir |
| OneDrive sync conflicts on heavy `/shared` writes | Keep Dropbox for handoff files, not active work trees — work happens in `/workspace` |
| Ray's Claude can read everything in `/workspace` + `/shared` | That's all Ray's own data — boundary intact. Hermes `.env`/auth deliberately NOT mounted |
| Billing surprise for Ray | Phase 0 decision: Ray's own plan; usage limits are his to manage |

---

## 7. Decisions (resolved 2026-06-09)

1. **Subscription:** Ray has claude.ai Pro — prerequisite met, he owns the billing.
2. **Session spawn mode:** `--spawn same-dir` (the default) — single shared workspace, no git-worktree mode.
3. **Workspace:** Hermes and Claude Code share `/workspace` — same pattern as Claude Code + Hermes sharing the ned repo on Neima's side. AGENTS.md conventions (Phase 4) keep the two agents coordinated.
