# Home Assistant MCP Setup
*Verified 2026-05-29 from Mac Mini Hermes runtime*

---

## Current Status

Home Assistant is connected to Hermes through the official Home Assistant **Model Context Protocol Server** integration using Hermes native HTTP MCP support.

Verified state:

- Home Assistant root URL: `http://homeassistant.local:8123` → HTTP 200
- Home Assistant MCP endpoint: `http://homeassistant.local:8123/api/mcp`
  - unauthenticated request → HTTP 401, which confirms the endpoint exists and requires auth
- Hermes MCP server name: `homeassistant`
- Hermes transport: native HTTP / Streamable HTTP via `url:` config
- `mcp-proxy`: not used
- `~/.hermes/.env` has exactly one `HA_MCP_URL`, one `HA_MCP_TOKEN`, and one `HA_MCP_TIMEZONE` entry after token refresh
- `hermes mcp test homeassistant` connects successfully and discovers 20 tools
- Fresh Hermes CLI read-only validation using `GetLiveContext` succeeds
- Hermes gateway was restarted after the token refresh so platform sessions inherit the working MCP setup

## Local Secret Storage

Secrets are local only in the Hermes profile env file:

```bash
~/.hermes/.env
```

Expected variable names:

```bash
HA_MCP_URL=http://homeassistant.local:8123
HA_MCP_TOKEN=[REDACTED]
HA_MCP_TIMEZONE=America/Chicago
```

Do not commit the token or paste it into chat.

## Hermes MCP Config Shape

The active config in `~/.hermes/config.yaml` uses this shape:

```yaml
mcp_servers:
  homeassistant:
    url: "http://homeassistant.local:8123/api/mcp"
    headers:
      Authorization: "Bearer ${HA_MCP_TOKEN}"
    timeout: 120
    connect_timeout: 60
```

## Verification Commands and Results

Commands run:

```bash
hermes mcp test homeassistant
hermes chat -q "Use the Home Assistant MCP server only for read-only validation..."
hermes gateway restart
```

`hermes mcp test homeassistant` result:

- connected successfully in ~47 ms
- discovered 20 tools

Discovered tool names from the official HA MCP server:

- `HassTurnOn`
- `HassTurnOff`
- `HassCancelAllTimers`
- `HassMediaUnpause`
- `HassMediaPause`
- `HassMediaNext`
- `HassMediaPrevious`
- `HassSetVolume`
- `HassSetVolumeRelative`
- `HassMediaPlayerMute`
- `HassMediaPlayerUnmute`
- `HassMediaSearchAndPlay`
- `HassLightSet`
- `HassBroadcast`
- `HassListAddItem`
- `HassListCompleteItem`
- `HassListRemoveItem`
- `GetDateTime`
- `todo_get_items`
- `GetLiveContext`

## Read-Only Validation Result

A fresh Hermes CLI session successfully called only the read-only `GetLiveContext` tool.

Confirmed validation result:

- MCP initialize: HTTP 200
- server name: `home-assistant`
- server version: `1.26.0`
- `GetLiveContext` call: HTTP 200
- result success: `true`
- write/control/media/broadcast/todo mutation tools: not called

Observed live context examples:

- Entry Lamp / Entryway light: on, brightness 143
- Family Room light: on, brightness 66
- Family Room Main Lights: off
- TV lightstrip: on, brightness 66
- 75" The Frame in Family Room: on, volume 0.12
- Living Room media player: playing TV / TV Audio
- Garage media player: paused, “Tweaker” by GELO, volume 0.27
- Listening Room light: on, brightness 65
- Listening Room media player: paused, “You Should Probably Leave” by Chris Stapleton, volume 0.47
- Kitchen Main Lights / Kitchen Island Pendants: off
- Shopping List todo entity: state 0

This proves Hermes can answer “what lights are on?” from live Home Assistant state, not from the static Ned entity map.

## Safety Notes

The official HA MCP server exposes both read and write-capable tool names. Keep these rules until Neima explicitly approves a first write test:

- Use `GetLiveContext`, `GetDateTime`, and read-only todo queries for normal status questions.
- Do not call `HassTurnOn`, `HassTurnOff`, `HassLightSet`, media control, broadcast, or todo mutation tools without explicit approval in the current turn.
- Keep the first write test limited to one visible, low-risk light or scene.
- Avoid locks, cameras/security, HVAC, arbitrary service calls, automation/config mutation, and unbounded Sonos volume.

## Ned Safe MCP Surface

Default allowlist for Hermes/Ned when HA MCP is connected:

### Read
- `GetLiveContext`
- `GetDateTime`
- read-only todo queries when useful

### Write
- `script.family_room_evening`
- `script.family_room_movie`
- `script.all_house_lights_off`
- other exact scripts explicitly added later

### Off-limits for casual use
- locks and garage doors
- cameras and security devices
- HVAC and thermostat changes
- broad automation/config edits
- arbitrary `call_service` style control
- unbounded media volume/playback control
- room-wide actions that need interpretation instead of an exact target

Rule of thumb: if it is ambiguous, it does not get agent write access yet.

## First Write Test Result

Completed 2026-05-29 with explicit user approval.

Approved scope:

- Target: `light.family_room_main_lights` / "Family Room Main Lights"
- Requested action: turn on to 30% brightness

MCP write call:

- Tool: `HassLightSet`
- Arguments: `name="Family Room Main Lights"`, `area="Family Room"`, `domain=["light"]`, `brightness=30`
- Result: `action_done`, success included `light.family_room_main_lights`

Read-only verification:

- Tool: `GetLiveContext`
- Result after propagation: Family Room Main Lights `on`, brightness `76` raw HA brightness, approximately 30% of 255.

Important safety observation:

- Because the official MCP tool uses natural-language Home Assistant Assist targeting, including `area="Family Room"` appears to have affected the broader Family Room light area as well as the named entity.
- Follow-up live read showed nearby Family Room lights also around 30% raw brightness (`light.family_room`, `light.family_room_lamp`, and `light.tv_lightstrip`).
- For future write tests, use the narrowest selector possible and consider an allowlisted wrapper if exact entity-only writes are required.

## First-Pass MCP Operating Checklist

Use this as the default day-to-day checklist when Hermes/Ned talks to Home Assistant.

1. Start with `GetLiveContext` for live status questions.
2. Use `GetDateTime` only when time context matters.
3. Interpret live state through `references/home-assistant-entity-map.md`, not as a raw entity dump.
4. For normal home control, prefer the explicit approved script surface:
   - `script.family_room_evening`
   - `script.family_room_movie`
   - `script.all_house_lights_off`
5. If a new action is needed, add it to the allowlist before using it casually.
6. For any write, verify the state immediately after the action.
7. If the request is ambiguous, stop and clarify rather than guessing.
8. Keep locks, cameras/security, HVAC, and arbitrary service calls out of routine agent use.

## Next Steps

1. Decide whether to keep official HA MCP write access as approval-gated natural-language control, or build a small allowlisted wrapper for exact entity-only writes.
2. Continue Phase 3 with the custom Ned MCP server and the first Hermes cron health brief.

Completed follow-up:

- `references/home-assistant-entity-map.md` was cross-checked against `GetLiveContext` on 2026-05-29 and refreshed as a curated agent map, not a raw entity dump.
