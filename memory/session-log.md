<!-- Session observation log. Format: [YYYY-MM-DD] [type] observation -->
[2026-06-08] [project] Hermes/Ned migrated from Mac Mini to Windows PowerSpec (Neima_Server, 192.168.68.89, Tailscale 100.120.157.4). Gateway installed as Windows Scheduled Task. Mac Mini gateway stopped.
[2026-06-08] [project] Ray Hermes Docker container also migrated to Windows server (was on Mac Mini). Container at C:\hermes-friends\ray\, bound 100.120.157.4:8643. Mac container stopped.
[2026-06-08] [project] Windows server primary host confirmed: Hermes v0.16.0, 67 sessions carried over, SOUL.md written, gateway Scheduled Task active, Telegram confirmed live.
[2026-06-08] [user] Hostname preference: Neima_Server (not ned-server as originally planned in migration doc).
[2026-06-08] [project] HA not yet migrated — Mac Mini still hosting HAOS VM at 192.168.68.85:8123. Hermes MCP URL updated to point at Mac Mini IP. HA migration to Windows (Hyper-V/Docker) is Phase 9, intentionally deferred.
[2026-06-08] [project] Cron bash scripts (mac-mini-health-brief.sh, ray-hermes-health-brief.sh) deferred for rewrite — will fail on Windows until rebuilt as .py or .ps1.
<!-- Cleared automatically when /note is run. -->
[2026-05-29] [project] Reboot test complete: Hermes gateway, Tailscale, and Ollama auto-start; Docker Desktop needs `open -a Docker`; HAOS UTM VM `Linux` needs `utmctl start 'Linux'` before `homeassistant.local:8123` returns 200.
[2026-05-29] [project] HA entity map generated and saved to references/home-assistant-entity-map.md — live snapshot of all devices
[2026-05-29] [user] HA setup: Hue (Family Room, Entryway, Listening Room), Lutron Caseta (Master Bedroom, Dining Room, Kitchen, Family Room, Guestroom, Exterior), Sonos (Living Room, Listening Room, Office, Garage, Neima's Room), Samsung TVs (75" The Frame, 65" OLED), Music Assistant installed
[2026-05-29] [user] listening_room_lamp unavailable = intentional (off at switch); 65" OLED unavailable = rarely used TV, expected
[2026-05-29] [project] Home Assistant official MCP Server is connected to Hermes via native HTTP; read-only GetLiveContext validation passed; writes remain approval-gated.
[2026-05-29] [project] First approved HA MCP write test completed: Family Room Main Lights set to ~30%; official MCP Assist targeting also affected nearby Family Room lights, so future writes should use narrower selectors or an allowlisted wrapper.
[2026-05-29] [project] Telegram family-room-off follow-up revealed Hue group targeting missed separate Lutron main lights. Exact entity turn-off fixed all Family Room lights off; entity map now documents the four-entity Family Room set.
[2026-05-29] [project] HA MCP token stored in ~/.hermes/.env (single clean entry); config in ~/.hermes/config.yaml under mcp_servers.homeassistant; setup docs in references/ha-mcp-setup.md
[2026-05-30] [user] Home network: AT&T Fiber gateway radios off/IP-passthrough-style bridge via multi-gig to main Deco BE63 2.5GbE; BE63 feeds 2.5GbE 8-port switch, three additional Deco nodes, and Luxul 16-port gigabit switch for home Ethernet.
[2026-05-31] [user] Hermes Agent uninstalled from MBP — rm -rf ~/.hermes && rm ~/.local/bin/hermes
[2026-05-31] [project] Mac Mini SMB hardening complete: authenticated `Neima Home Folder` share active, guest SMB access disabled, FileVault remains off, macOS firewall and stealth mode enabled.
[2026-05-31] [project] Roadmap activation status cleaned up: HA MCP live read access + entity map cross-check are complete; custom Ned MCP server and daily health brief cron are next.
[2026-05-31] [user] AT&T Fiber gateway model confirmed as BGW320-500.
[2026-05-31] [project] Roadmap updated: Home Assistant usability is now a required near-term milestone — Companion App, phone dashboard, scenes, and practical automations must make HA useful vs Google Home / Apple Home before deeper expansion.
[2026-05-31] [project] HA usability scope expanded: inventory/migrate existing Google Home, Lutron, and Hue automations/scenes into HA so HA becomes the main smart-home control plane rather than another parallel app.
[2026-05-31] [project] UniFi skill assessment: the found `unifi-cli` file is only an inventory/API helper; it does not replace a safe UDM cutover plan covering DHCP, VLANs, firewall rules, smart-home discovery, and rollback.
[2026-05-31] [project] Roadmap updated: add hybrid AI provider lane — Hermes/OpenAI via current ChatGPT OAuth subscription remains primary Ned operator; Claude subscription becomes second-brain lane for plans/architecture/docs/code review; local Ollama/llama.cpp models are scoped to simple/private/offline worker tasks.
[2026-05-31] [project] Roadmap updated: Grok/xAI OAuth added as a possible cloud contingency lane for Hermes if support proves stable, alongside OpenAI primary, Claude second-brain, and local simple-worker models.
[2026-06-01] [project] Mac Mini active LAN is UGREEN 2.5GbE adapter en9; HAOS UTM bridge must target en9, not stale en0.
[2026-06-01] [project] First daily Hermes health brief cron created for Ned Telegram group using repo script scripts/mac-mini-health-check.sh.
[2026-06-01] [project] Home Assistant usability pass started: first mobile dashboard/scene plan and Google/Hue/Lutron inventory template created in Ned repo.
[2026-06-01] [project] Smart home inventory captured: Apple Home Evening/Movie, Google Home 11 PM All Lights Off, Hue Morning/Evening Lamps, and Lutron outdoor schedules; first HA migration target is Evening then Movie.
[2026-06-04] [project] Roadmap updated: add Obsidian as Ned's human-facing knowledge layer for curated notes, decisions, runbooks, and research synthesis while keeping the ned Git repo as canonical agent source of truth.
[2026-06-04] [project] Roadmap dashboard added: `roadmap/roadmap.yaml` is now the canonical structured end-to-end roadmap; generated views live at `roadmap/index.html`, `roadmap/roadmap.csv`, `roadmap/roadmap.md`, and `roadmap/roadmap.json`. Reorder roadmap work by changing item `order` values and regenerating with `python3 scripts/generate-roadmap.py`.
[2026-06-04] [project] Ray × Neima AI Power Session agenda document created at `plans/ray-ai-power-session-agenda.html` to package the 2-day learning/build agenda into a browser/print-friendly artifact.
[2026-06-04] [project] Ray Hermes Tailscale/Desktop access enabled: Ray Docker API server exposed only on Mac mini Tailscale IP `100.106.154.18:8643` -> container `8642`, model name `ray-hermes`, bearer key stored in Ray isolated `.env`, and Ray connection instructions placed in Ray Dropbox outbox.
[2026-06-07] [user] Windows server NEIMA_SERVER SSH configured: LAN alias neima-server to 192.168.68.89, Tailscale alias neima-server-remote to 100.120.157.4; Hermes over SSH fixed by pointing hermes.cmd HERMES_PYTHON to system Python 3.13.
