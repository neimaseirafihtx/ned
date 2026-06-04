# Ned End-to-End Roadmap

Canonical structured roadmap for Ned: every known major roadmap item, including completed, active, planned, deferred, and conditional work.

> Generated from `roadmap/roadmap.yaml`. Reorder work by changing item `order` values, then run `python3 scripts/generate-roadmap.py`.

## Status summary

- **Done:** 5
- **Active:** 10
- **Next:** 1
- **Planned:** 8
- **Deferred:** 1
- **Conditional:** 1

## AI / Agents

### 10. Agent Foundation — Done (Phase 1)

Hermes running on the Mac mini with GPT-5.5/OpenAI path and Telegram access.

- **Next action:** Keep stable; monitor with health checks and update-readiness reports.
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

- **Next action:** Keep read access broad but interpret through curated entity map.
- **Sources:** plans/home-assistant-mcp-roadmap.md, references/ha-mcp-setup.md, memory/session-log.md

### 60. Approval-gated safe light control — Active (Phase 3)

Light writes have been tested, but routine control should use exact light entities or allowlisted scripts.

- **Next action:** Prefer deterministic scripts/entities for daily light actions; keep Sonos/TV/HVAC/security off-limits.
- **Depends on:** ha-mcp-read-access, ha-entity-map
- **Sources:** plans/home-assistant-mcp-roadmap.md, memory/session-log.md

### 70. Home Assistant human usability pass — Active (Phase 3)

Make HA useful for Neima day-to-day with Companion App, phone dashboard, scenes, and practical automations.

- **Next action:** Continue dashboard v2, source-app inventory, and tested scripts/scenes.
- **Depends on:** ha-entity-map, ha-safe-light-control
- **Sources:** plans/home-assistant-usability-pass.md, references/home-assistant-automation-inventory.md, memory/project_homelab_roadmap.md

### 80. Neima Home dashboard — Active (Phase 3)

HA dashboard created at /neima-home/home with room cards and Family Room script buttons.

- **Next action:** Refine card order, top quick actions, and remove rarely used/noisy entities.
- **Depends on:** ha-usability-pass
- **Sources:** plans/home-assistant-usability-pass.md

### 200. Smart-home automation migration — Planned (Phase 4)

Inventory and selectively migrate Google Home, Apple Home, Hue, and Lutron routines into Home Assistant after testing replacements.

- **Next action:** Finish automation inventory and choose first schedule/scene to migrate.
- **Depends on:** ha-usability-pass, neima-home-dashboard
- **Sources:** references/home-assistant-automation-inventory.md, plans/home-assistant-usability-pass.md

## Infrastructure / Mac mini / Network

### 20. Home Lab Substrate — Done (Phase 2)

Mac mini, SSH, Homebrew, Tailscale, Docker Desktop, UTM/HAOS, Ollama, and Ned repo baseline.

- **Next action:** Keep boot/reboot assumptions documented as services evolve.
- **Sources:** memory/project_homelab_roadmap.md, memory/session-log.md, references/home_server_handoff.md

### 30. Mac mini reboot/service baseline — Done (Phase 3)

Verified Hermes gateway, Tailscale, and Ollama auto-start; Docker Desktop and HAOS/UTM boot behavior documented.

- **Next action:** Revisit after Hermes updates, Docker changes, or UTM network changes.
- **Sources:** plans/mac-mini-ops-baseline.md, memory/session-log.md

### 90. Daily Mac mini homelab health brief — Active (Phase 3)

Script-only Hermes cron sends daily Mac mini/Ned health report to Neima's Telegram DM at 8:00 AM.

- **Next action:** Debug Home Assistant reachability separately when it fails in reports.
- **Sources:** scripts/mac-mini-health-check.sh, memory/session-log.md

### 100. Weekly Hermes update readiness check — Active (Phase 3)

Weekly non-mutating cron checks Hermes version, config, doctor, skills, and git ahead/behind state.

- **Next action:** Review Monday reports and run manual Hermes update when appropriate.
- **Sources:** ~/.hermes/scripts/hermes-update-check.py

### 210. Home Assistant boot/reachability reliability — Planned (Phase 4)

Make HAOS/UTM startup and homeassistant.local / 192.168.68.68 reachability reliable after reboots and bridge changes.

- **Next action:** Debug current HA reachability when Neima wants; verify UTM bridge targets en9.
- **Depends on:** mac-mini-reboot-baseline
- **Sources:** memory/session-log.md, memory/project_homelab_roadmap.md

### 250. Samsung T9 storage baseline / future Nextcloud lane — Active (Phase 4)

Samsung T9 is mounted and usable as Mac mini storage/agent workspace; Nextcloud remains a future service option.

- **Next action:** Define stable mount naming, backup conventions, and which folders/services should use the drive before installing persistent services on it.
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

Pilot a separate Hermes container for Ray with isolated Hermes home, workspace, Telegram bot, OpenAI OAuth, and OneDrive file handoff.

- **Next action:** Keep Ray isolated and document operational lessons before adding more friends.
- **Depends on:** mac-mini-substrate
- **Sources:** plans/friend-hermes-docker-roadmap.md, references/ray-hermes-agent-setup.md

### 180. Daily Ray Hermes health monitor — Active (Phase 5)

Script-only cron checks Ray Hermes container, gateway, pairing, mounts, resource usage, logs, compose dir, and OneDrive Dropbox.

- **Next action:** Watch daily 8:10 AM DM report and refine checks as Ray's usage changes.
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
