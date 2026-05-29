# Home Assistant MCP Setup
*Verified 2026-05-29 from Mac Mini Hermes runtime*

---

## Current Status

Home Assistant's official **Model Context Protocol Server** integration is installed and Hermes has a native HTTP MCP config for it, but the current stored token is not authenticating.

Verified state:

- Home Assistant root URL: `http://homeassistant.local:8123` → HTTP 200
- Home Assistant MCP endpoint: `http://homeassistant.local:8123/api/mcp`
  - unauthenticated request → HTTP 401, which confirms the endpoint exists and requires auth
- Hermes MCP server name: `homeassistant`
- Hermes transport: native HTTP / Streamable HTTP via `url:` config
- `mcp-proxy`: not used
- Hermes gateway: restarted after config change
- Current blocker: `hermes mcp test homeassistant` now returns HTTP 401 Unauthorized with the stored `HA_MCP_TOKEN`; `/api/` and `/api/config` also return 401 with all local `HA_MCP_TOKEN` entries.
- Action needed: regenerate or re-store the Home Assistant long-lived token for the dedicated `Hermes MCP` user, then re-run `hermes mcp test homeassistant`.

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

## Initial Discovery vs Current Auth State

During this session, an earlier `hermes mcp test homeassistant` reported a successful connection and discovered 20 tools, and a fresh Hermes CLI read-only prompt reported `GetLiveContext` output. A later verification pass failed with HTTP 401 for the same local token material, including direct Home Assistant REST checks against `/api/` and `/api/config`.

Treat the setup as **configured but blocked on valid token authentication** until a fresh token re-test passes.

Previously observed tool names from the official HA MCP server:

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

A read-only `GetLiveContext` response was observed earlier in the session, but follow-up verification now fails at token auth. Do not treat read-only validation as durable until `hermes mcp test homeassistant` succeeds again with a freshly stored token.

Previously observed live context examples:

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

This proves the server/tool path can work, but the current durable state is blocked on token authentication and needs a fresh successful `hermes mcp test homeassistant` before relying on live state.

## Safety Notes

The official HA MCP server exposes both read and write-capable tool names. Keep these rules until Neima explicitly approves a first write test:

- Use `GetLiveContext`, `GetDateTime`, and read-only todo queries for normal status questions.
- Do not call `HassTurnOn`, `HassTurnOff`, `HassLightSet`, media control, broadcast, or todo mutation tools without explicit approval in the current turn.
- Keep the first write test limited to one visible, low-risk light or scene.
- Avoid locks, cameras/security, HVAC, arbitrary service calls, automation/config mutation, and unbounded Sonos volume.

## Next Steps

1. Regenerate or re-store the Home Assistant long-lived token for the `Hermes MCP` user.
2. Re-run `hermes mcp test homeassistant`; expected result is connected + tools discovered, not HTTP 401.
3. After auth passes, compare `GetLiveContext` output against `references/home-assistant-entity-map.md` and refresh stale state notes without turning the map into a raw entity dump.
4. Ask Neima before the first write test.
5. If write testing is approved, use one visible low-risk target such as `light.tv_lightstrip` or `scene.entryway_relax`, then verify live state afterward.
6. Continue Phase 3 with the custom Ned MCP server and the first Hermes cron health brief.
