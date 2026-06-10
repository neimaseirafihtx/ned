# Ned End-to-End Roadmap

Canonical structured roadmap for Ned: every known major roadmap item, including completed, active, planned, deferred, and conditional work.

> Generated from `roadmap/roadmap.yaml`. Reorder work by changing item `order` values, then run `python3 scripts/generate-roadmap.py`.

## Status summary

- **Done:** 5
- **Active:** 8
- **Next:** 2
- **Planned:** 9
- **Deferred:** 1
- **Conditional:** 1

## AI / Agents

### 10. Agent Foundation — Done (Phase 1)

Hermes running with GPT-5.5/OpenAI path and Telegram access; migrated Mac mini → Windows server 2026-06-08.

- **Next action:** Keep stable on the Windows server; monitor with health checks and update-readiness reports.
- **Sources:** memory/project_homelab_roadmap.md, memory/session-log.md

### 110. Custom Ned MCP server — Planned (Phase 3)

Build a project/homelab status MCP server for Ned memory, roadmap, and infrastructure state.

- **Next action:** Revisit after the Obsidian knowledge layer has clarified Ned's human-facing notes, runbooks, and project status model.
- **Depends on:** ha-mcp-read-access, daily-mac-mini-health-brief
- **Sources:** memory/project_homelab_roadmap.md

### 140. Hybrid AI provider lane — Active (Phase 3)

OpenAI/ChatGPT remains primary Ned operator; Claude is second-brain/reviewer; Grok/xAI tracked as contingency; local models are supporting workers.

- **Next action:** Document routing rules as actual operational patterns emerge.
- **Sources:** memory/project_homelab_roadmap.md, memory/session-log.md

### 150. Claude second-brain review lane — Planned (Phase 5)

Use Claude deliberately for planning, architecture, long-context docs, code review, and careful second opinions.

- **Next action:** Define handoff templates and when Hermes should ask Claude/Claude Code for review.
- **Depends on:** hybrid-ai-provider-lane
- **Sources:** memory/project_homelab_roadmap.md

## Home Assistant / Smart Home

### 40. Home Assistant entity map — Done (Phase 3)

Room/device map generated, curated, and cross-checked against live HA MCP state.

- **Next action:** Update when new HA devices/entities are added or renamed.
- **Sources:** references/home-assistant-entity-map.md, memory/session-log.md

### 50. Home Assistant MCP read access — Done (Phase 3)

Official HA MCP Server connected to Hermes via native HTTP; read-only validation passed.

- **Next action:** HA offline since Mac mini decommission — after HA restore on Windows, mint a new token, update Hermes .env, and re-validate with `hermes mcp test homeassistant`.
- **Sources:** plans/home-assistant-mcp-roadmap.md, references/ha-mcp-setup.md, memory/session-log.md

### 60. Approval-gated safe light control — Active (Phase 3)

Light writes have been tested, but routine control should use exact light entities or allowlisted scripts.

- **Next action:** Paused — HA offline until restored on the Windows server. Then prefer deterministic scripts/entities for daily light actions; keep Sonos/TV/HVAC/security off-limits.
- **Depends on:** ha-mcp-read-access, ha-entity-map, home-assistant-boot-reliability
- **Sources:** plans/home-assistant-mcp-roadmap.md, memory/session-log.md

### 70. Home Assistant human usability pass — Active (Phase 3)

Make HA useful for Neima day-to-day with Companion App, phone dashboard, scenes, and practical automations.

- **Next action:** Paused — HA offline until restored on the Windows server. Then continue dashboard v2, source-app inventory, and tested scripts/scenes.
- **Depends on:** ha-entity-map, ha-safe-light-control, home-assistant-boot-reliability
- **Sources:** plans/home-assistant-usability-pass.md, references/home-assistant-automation-inventory.md, memory/project_homelab_roadmap.md

### 80. Neima Home dashboard — Active (Phase 3)

HA dashboard created at /neima-home/home with room cards and Family Room script buttons.

- **Next action:** Paused — HA offline until restored on the Windows server (dashboard config is inside the HA backup). Then refine card order and quick actions.
- **Depends on:** ha-usability-pass, home-assistant-boot-reliability
- **Sources:** plans/home-assistant-usability-pass.md

### 200. Smart-home automation migration — Planned (Phase 4)

Inventory and selectively migrate Google Home, Apple Home, Hue, and Lutron routines into Home Assistant after testing replacements.

- **Next action:** Finish automation inventory and choose first schedule/scene to migrate.
- **Depends on:** ha-usability-pass, neima-home-dashboard
- **Sources:** references/home-assistant-automation-inventory.md, plans/home-assistant-usability-pass.md

## Infrastructure / Windows Server / Network

### 20. Home Lab Substrate — Done (Phase 2)

Original Mac mini substrate (SSH, Homebrew, Tailscale, Docker, UTM/HAOS, Ollama, Ned repo); re-platformed to the Windows server 2026-06-08, Mac mini decommissioned/returned 2026-06-09.

- **Next action:** Historical — current substrate is the Windows server (memory/user_windows_server.md).
- **Sources:** memory/project_homelab_roadmap.md, memory/session-log.md, references/home_server_handoff.md

### 30. Mac mini reboot/service baseline — Done (Phase 3)

Verified Hermes gateway, Tailscale, and Ollama auto-start on the Mac mini; superseded by the Windows server migration.

- **Next action:** Historical — build an equivalent Windows server ops baseline (Scheduled Task, Docker, Ollama, Tailscale, reboot survival).
- **Sources:** plans/mac-mini-ops-baseline.md, memory/session-log.md

### 90. Daily homelab health brief (Windows rewrite) — Planned (Phase 3)

Mac mini version retired with the machine (2026-06-09); rewrite the daily Hermes health cron for the Windows server (Hermes task, Ray container, Ollama, Tailscale, disk, and HA once restored).

- **Next action:** Rewrite scripts/mac-mini-health-check.sh as a .ps1/.py Windows host check and re-register the 8:00 AM Hermes cron.
- **Sources:** scripts/mac-mini-health-check.sh, memory/session-log.md

### 100. Weekly Hermes update readiness check — Active (Phase 3)

Weekly non-mutating cron checks Hermes version, config, doctor, skills, and git ahead/behind state.

- **Next action:** Review Monday reports and run manual Hermes update when appropriate.
- **Sources:** ~/.hermes/scripts/hermes-update-check.py

### 210. Restore Home Assistant on the Windows server — Next (Phase 4)

HA is offline since the Mac mini was decommissioned (2026-06-09). Rebuild as a Hyper-V HAOS x86_64 VM, restore the full backup from C:\restore\home-assistant\backups\, reconnect Hue/Caseta/Sonos, and re-point Hermes MCP.

- **Next action:** Enable Hyper-V, create the HAOS x86_64 VM with an external (LAN-bridged) switch, restore automatic_backup_2026_5_4.tar, then mint a new long-lived token for Hermes MCP.
- **Sources:** home-assistant-windows-migration-handoff-2026-06-08.md, memory/user_windows_server.md

### 250. Samsung T9 storage baseline / future Nextcloud lane — Planned (Phase 4)

Samsung T9 was the Mac mini's storage/agent workspace; the Mac mini is gone (2026-06-09), so the drive needs a new role on the Windows server. Nextcloud remains a future service option.

- **Next action:** Attach the T9 to the Windows server, verify contents, and define mount/backup conventions before installing persistent services on it.
- **Sources:** memory/project_homelab_roadmap.md

## Knowledge / Obsidian / Docs

### 120. Interactive end-to-end roadmap dashboard — Active (Phase 3)

Structured roadmap data plus generated CSV, Markdown, JSON, and local HTML dashboard for viewing/reordering Ned work.

- **Next action:** Use roadmap/roadmap.yaml order fields or dashboard export to reprioritize.
- **Depends on:** agent-foundation
- **Sources:** roadmap/roadmap.yaml, roadmap/index.html

### 130. Obsidian knowledge layer — Next (Phase 5)

Human-facing Ned vault for curated notes, decisions, runbooks, research synthesis, and memory-palace navigation.

- **Next action:** Design vault folders, boundaries, and constrained agent write areas before enabling write access.
- **Depends on:** roadmap-dashboard
- **Sources:** memory/project_homelab_roadmap.md, memory/session-log.md

## Friend Hermes / Hosted Agents

### 170. Docker-isolated friend Hermes pilot — Active (Phase 5)

Separate Hermes container for Ray with isolated Hermes home, workspace, Telegram bot, OpenAI OAuth, and OneDrive file handoff; migrated to the Windows server 2026-06-08 (C:\hermes-friends\ray\).

- **Next action:** Keep Ray isolated and document operational lessons before adding more friends.
- **Depends on:** mac-mini-substrate
- **Sources:** plans/friend-hermes-docker-roadmap.md, references/ray-hermes-agent-setup.md

### 180. Daily Ray Hermes health monitor — Active (Phase 5)

Script-only cron checks Ray Hermes container, gateway, pairing, mounts, resource usage, logs, compose dir, and OneDrive Dropbox.

- **Next action:** Port ray-hermes-health-brief.sh to the Windows server (.ps1/.py) and re-register the 8:10 AM cron — the bash version targeted the decommissioned Mac mini.
- **Depends on:** friend-hermes-docker-pilot
- **Sources:** references/ray-hermes-agent-setup.md, ~/.hermes/scripts/ray-hermes-health-brief.sh

### 190. Friend Hermes template / repeatable onboarding — Planned (Phase 5)

Turn Ray's proven one-off setup into a reusable template for future isolated friend Hermes instances.

- **Next action:** Extract Ray compose/config/checklist into a parameterized friend Hermes template with security verification.
- **Depends on:** friend-hermes-docker-pilot, ray-hermes-health-monitor
- **Sources:** plans/friend-hermes-docker-roadmap.md

## Local Models / Sovereignty

### 160. Local simple-task workers — Planned (Phase 5)

Use Ollama/llama.cpp workers for simple, fast, private, or offline tasks rather than replacing the cloud chief-of-staff model.

- **Next action:** Identify first low-risk local tasks such as log triage or structured extraction.
- **Depends on:** hybrid-ai-provider-lane
- **Sources:** memory/project_homelab_roadmap.md

### 220. Local intelligence layer — Planned (Phase 4)

Expand local inference/automation capacity after Phase 3 foundation, scoped to proven useful tasks.

- **Next action:** Revisit after HA usability and custom Ned MCP server are stable.
- **Depends on:** custom-ned-mcp-server, local-simple-task-workers
- **Sources:** memory/project_homelab_roadmap.md

### 260. Mastery + sovereignty — Planned (Phase 7)

Long-term hybrid cloud/local stack with fully local components where quality, context, latency, and reliability make sense.

- **Next action:** Accumulate lessons from MCP, cron, friend Hermes, local workers, and HA automation work.
- **Depends on:** hybrid-ai-provider-lane, local-intelligence-layer
- **Sources:** memory/project_homelab_roadmap.md

## Future Expansion

### 230. Camera / Frigate / NVR path — Deferred (Phase 4)

Local camera/NVR work is intentionally postponed; Nest cameras/thermostats remain deferred for now.

- **Next action:** Do not plan storage or GPU around cameras until Neima explicitly reopens this project.
- **Sources:** memory/project_homelab_roadmap.md

### 240. GPU stack — Conditional (Phase 6)

GPU/NVR/local-heavy stack only triggers if there is a full Nest-to-Reolink/local-camera migration or proven local inference need.

- **Next action:** Keep conditional; do not buy/build until trigger criteria are met.
- **Depends on:** camera-frigate-nvr
- **Sources:** memory/project_homelab_roadmap.md
