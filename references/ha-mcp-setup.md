# Home Assistant MCP Setup
*Verified 2026-05-29 from Mac Mini Hermes runtime*

---

## Current Status

Home Assistant is connected to Hermes through the official Home Assistant **Model Context Protocol Server** integration.

Verified state:

- Home Assistant root URL: `http://homeassistant.local:8123` → HTTP 200
- Home Assistant MCP endpoint: `http://homeassistant.local:8123/api/mcp`
  - unauthenticated request → HTTP 401, which confirms the endpoint exists and requires auth
- Hermes MCP server name: `homeassistant`
- Hermes transport: native HTTP / Streamable HTTP via `url:` config
- `mcp-proxy`: not used
- Hermes gateway: restarted after config change
- Read-only validation: passed with `GetLiveContext`

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
hermes mcp list
hermes mcp test homeassistant
hermes chat -q "Use the Home Assistant MCP server only for a read-only validation..."
```

`hermes mcp test homeassistant` result:

- connected successfully in ~72 ms
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

Confirmed live context examples at validation time:

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

## Next Steps

1. Compare `GetLiveContext` output against `references/home-assistant-entity-map.md` and refresh stale state notes without turning the map into a raw entity dump.
2. Ask Neima before the first write test.
3. If write testing is approved, use one visible low-risk target such as `light.tv_lightstrip` or `scene.entryway_relax`, then verify live state afterward.
4. Continue Phase 3 with the custom Ned MCP server and the first Hermes cron health brief.
