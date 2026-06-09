# Ray Hermes Agent — Mac Mini → Windows Migration Handoff

**Date:** 2026-06-08
**Goal:** Move Ray's Hermes agent + its Docker container from the Mac Mini to the Windows server (NEIMA_SERVER), preserving Ray's memory, pairing, cron, and config.
**Status:** ✅ Build verified, resources/rename done, Ray's state confirmed intact. **Cutover steps remaining** (stop Mac → restart Windows → Telegram test — see bottom).

---

## Final state

| Item | Value |
|---|---|
| New host | Windows server, Tailscale IP `100.120.157.4` |
| Old host | Mac Mini, Tailscale IP `100.106.154.18` (retired for Ray) |
| Container | `ray-hermes`, image `ray-hermes:latest`, `Up`, bound `100.120.157.4:8643->8642` |
| Compose project | `ray-hermes` (network `ray-hermes_default`) — renamed from default `compose` |
| Resources | `mem_limit: 2g`, `cpus: "2.0"` |
| Hermes version | `0.16.0` (rebuilt fresh; Mac was on ~0.15.1) |
| Windows data root | `C:\hermes-friends\ray\` (`compose\`, `hermes-home\`, `workspace\`) |
| Shared `/shared` | `C:\Users\neima\OneDrive\Ray Dropbox` (live OneDrive-synced, not a static copy) |
| Telegram bot | `@Trismegis_bot` |
| Approved user | Ray Fitzgerald, telegram ID `8614345033` |

---

## How clean was Ray's memory / file transfer?

**Verdict: clean.** Ray keeps his identity, memory, pairing, cron, and config. Details below, including the one caveat worth recording honestly.

### Verified intact (read correctly through the rebuilt + recreated container)
- **`state.db` (24MB)** — sessions, conversation memory, agent state. Full size, not reset.
- **`auth.json` (5.4KB), `.env`, `config.yaml` (10KB), `SOUL.md`** — Ray's real files, not the install templates. (The image writes templates to `/home/hermes/.hermes`, but the compose `HERMES_HOME` override points Ray at the mounted `hermes-data`, so his real files win.)
- **Cron — all 3 AT100 jobs active** with correct schedules, workdirs (`/shared/2026 AT 100`), and **preserved last-run timestamps** — strong evidence the DB carried over rather than being re-initialized.
- **Telegram pairing** — Ray Fitzgerald / `8614345033` still approved.

### The one caveat: SQLite WAL
The backup was taken **after** stopping the Mac container (correct procedure), so SQLite's write-ahead log (`state.db-wal`, 5.9MB) should have checkpointed into `state.db` on the clean stop. All reads verify, which indicates it did. The only theoretical risk is that the last handful of interactions immediately before the backup lived solely in the WAL and didn't checkpoint — low probability given the clean stop, and not observed in verification. Recorded for completeness, not a known loss.

### The problem that occurred and was fixed: macOS `._` files
The Mac-made tarball included AppleDouble sidecar files (`._name`, `.__name`) for every file. These are inert on Windows/Linux **except** when an app globs a directory and tries to parse them — Hermes' pairing store did exactly that and crashed with `UnicodeDecodeError: ... byte 0x90`. Fixed by deleting all `._*` / `.__*` files inside the container. Pairing then read clean. **Will not recur** — nothing on Windows regenerates these files.

### Ongoing sync (going forward, not the one-time copy)
`/shared` is mounted to the live OneDrive `Ray Dropbox` folder, so inbox/outbox/working/archive stay in sync across machines automatically — no manual copying. Caveat: the folder must be pinned **"Always keep on this device"** so the container never reads empty cloud placeholders (see watch-list).

---

## Migration principle used

Containers are disposable; durable value lives in the bind-mounted folders. So: **rebuild the image fresh on Windows, preserve `hermes-home` / `workspace` / `compose` / Ray Dropbox.** Docker Desktop's internal VM was *not* migrated.

---

## What was done, in order

1. **Windows prep** — Installed Docker Desktop. WSL missing → `wsl --install`, reboot, WSL2 default. Docker verified clean.
2. **Mac backup** — Stopped `ray-hermes`, tarred the friend root, checksummed, restarted Ray on the Mac so it stayed live as source of truth:
   - `ray-hermes-friend-root-20260608T163140Z.tar.gz` (124M, `sha256sum -c` OK)
3. **Transfer** — SSH into Windows unavailable; moved the tarball manually to `C:\Users\neima\Documents\ray-migration-export`. Checksum re-verified OK after transfer.
4. **Extract** — `tar -xzf` into `C:\hermes-friends`. Windows `tar.exe` failed on Linux symlinks under `hermes-home/node` + `hermes-home/lsp` — **expected/harmless** (Dockerfile rebuilds those runtimes). Deleted both dirs.
5. **Compose edit** — Tailscale IP `100.106.154.18` → `100.120.157.4`; volume paths → `C:/...`; OneDrive `/shared` mount.
6. **Build** — `docker compose build --no-cache`. Hermes 0.16.0, 94 Python deps, 75 skills. Non-issues: `npm install failed` (browser tools, skipped via `--skip-browser`) and ffmpeg missing (TTS only).
7. **Start + verify** — Container `Up`, gateway running, state mounted, cron survived.
8. **Fixed pairing corruption** — purged `._*`/`.__*` (see above). Pairing then listed Ray approved.
9. **Resources + rename** — Set `mem_limit: 2g`, added `name: ray-hermes`. Recreate hit a stale-container name conflict (old `compose` project's container lingered after the project rename); resolved with `docker rm -f ray-hermes` then `docker compose up -d`. Verified: network `ray-hermes_default`, memory `2147483648` (2GB), pairing intact, gateway clean (no "draining" line).

---

## Adjusting resources later (reference)

**Per-container (Ray only)** — edit compose, then `docker compose up -d --force-recreate`:
```yaml
    mem_limit: 2g
    cpus: "2.0"
```
**Global WSL2 ceiling** — on WSL2 backend, Docker Desktop's Resources sliders are managed by WSL. Cap the whole VM via `C:\Users\neima\.wslconfig`:
```ini
[wsl2]
memory=8GB
processors=4
```
Then `wsl --shutdown` and restart Docker Desktop. (Not needed for the current 2g per-container setting.)

**Renaming the compose project** — set `name:` at the top of `docker-compose.yml` (not the folder). After a rename, the old project's container can linger and cause a name conflict on `up`; clear it with `docker rm -f ray-hermes`, then `docker compose up -d`.

---

## Remaining cutover steps

1. **Stop the Mac container** (prevents two gateways fighting over the Telegram token):
   ```
   docker stop ray-hermes        # on the Mac Mini
   docker ps --filter name=ray-hermes
   ```
2. **Bounce the Windows gateway** so it grabs the Telegram long-poll cleanly:
   ```
   docker restart ray-hermes
   docker exec ray-hermes hermes gateway status
   ```
3. **Live test** — send a fresh Telegram message to `@Trismegis_bot`; confirm Windows Ray replies. (This proves gateway + pairing + auth + model call end to end.)
4. **API health (optional):**
   ```
   curl http://100.120.157.4:8643/health
   ```

---

## Post-cutover cleanup

- Leave the **Mac container stopped** (don't delete) for a few days as rollback. Once Windows Ray is proven stable: `docker rm ray-hermes` on the Mac.
- **Update Ray's Desktop connection:** endpoint `http://100.120.157.4:8643`, model `ray-hermes`, existing `API_SERVER_KEY` from his `.env`. Old Mac endpoint `100.106.154.18:8643` is dead.
- **Backup tarball:** `C:\Users\neima\Documents\ray-migration-export\` — keep until cutover confirmed, then archive or delete.

---

## Watch-list / open items

- **OneDrive `/shared` placeholders:** confirm `Ray Dropbox` + subfolders are pinned local ("Always keep on this device") so the container never reads empty cloud placeholders. Cron last-run timestamps show `/shared` was readable; confirm the pin held.
- **Version bump 0.15.1 → 0.16.0:** no schema issues seen; watch first few cron runs and Telegram exchanges.
- **`.git` inside Ray Dropbox:** backup remote only, not the live sync path (OneDrive is). Low risk; watch for OneDrive conflict-copy files if Ray ever auto-commits.
- **Future Mac→anywhere tarballs:** suppress AppleDouble files at creation with `COPYFILE_DISABLE=1 tar ...`, or purge `._*`/`.__*` after extraction.
- **Do NOT** run both Mac and Windows gateways simultaneously long-term.
- **Do NOT** put `.env` / `auth.json` / API key / bot token into Git, OneDrive notes, or any repo.

---

## Security boundaries (carried over)

Ray's container must never mount: Neima's home folder, default `~/.hermes`, SSH keys, Home Assistant creds, the Docker socket, or the Ned repo. Runs with `no-new-privileges`, 2G mem limit, 2 CPU.
