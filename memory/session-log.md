<!-- Session observation log. Format: [YYYY-MM-DD] [type] observation -->
<!-- Cleared automatically when /note is run. -->
[2026-05-29] [project] Reboot test complete: Hermes survives, HAOS does not auto-restart (UTM LaunchAgent fix deferred)
[2026-05-29] [project] HA entity map generated and saved to references/home-assistant-entity-map.md — live snapshot of all devices
[2026-05-29] [user] HA setup: Hue (Family Room, Entryway, Listening Room), Lutron Caseta (Master Bedroom, Dining Room, Kitchen, Family Room, Guestroom, Exterior), Sonos (Living Room, Listening Room, Office, Garage, Neima's Room), Samsung TVs (75" The Frame, 65" OLED), Music Assistant installed
[2026-05-29] [user] listening_room_lamp unavailable = intentional (off at switch); 65" OLED unavailable = rarely used TV, expected
[2026-05-29] [project] Home Assistant official MCP Server is connected to Hermes via native HTTP; read-only GetLiveContext validation passed; writes remain approval-gated.
[2026-05-29] [project] First approved HA MCP write test completed: Family Room Main Lights set to ~30%; official MCP Assist targeting also affected nearby Family Room lights, so future writes should use narrower selectors or an allowlisted wrapper.
[2026-05-29] [project] Telegram family-room-off follow-up revealed Hue group targeting missed separate Lutron main lights. Exact entity turn-off fixed all Family Room lights off; entity map now documents the four-entity Family Room set.
