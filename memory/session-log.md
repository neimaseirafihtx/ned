<!-- Session observation log. Format: [YYYY-MM-DD] [type] observation -->
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
