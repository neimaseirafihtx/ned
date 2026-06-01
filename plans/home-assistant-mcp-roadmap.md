# Home Assistant MCP Roadmap

> **For Claude / Hermes:** This is the shared implementation roadmap for bringing Home Assistant into the agentic workflow. Treat the first session as read-only unless Neima explicitly approves a write test.

**Goal:** Connect Hermes to Home Assistant through MCP so agents can read live smart-home state, compare it against the curated entity map, and later perform tightly scoped safe controls.

## Operational Rule (read before wiring any token)

During initial setup, Hermes may only READ Home Assistant state. Any write action requires Neima to approve the exact `entity_id` and action in the current turn.

Generic service-call tools (`call_service` and anything that can create automations, helpers, dashboards, or scripts) must NOT be enabled for routine use unless they are wrapped, allowlisted, or documented as safe. If reads and writes cannot be separated into distinct tools, the server does not get persistent write access — full stop.

**Architecture:** There are three different Home Assistant MCP implementations and they are easy to confuse:

1. Official **Model Context Protocol Server** integration — a custom component installed INTO Home Assistant. HA acts as the server; control runs through the Assist API; you pick exactly which entities/services are exposed from the Exposed Entities page. This is the structural allowlist we want, and it is first-party.
2. Official **Model Context Protocol** integration — the reverse direction: HA as a client consuming other MCP servers. Not what we need here.
3. Community **ha-mcp** (`homeassistant-ai/ha-mcp`) — connects via REST + WebSocket and can create automations/helpers/dashboards. This is the most powerful and least safe option, not a read-only starter.

Start with the official MCP Server integration and expose ONLY a read-relevant entity set. Treat `ha-mcp` as a later, deliberately scoped option for structural work, never the first-session default.

**Tech Stack:** Hermes Agent native MCP HTTP client, Home Assistant official MCP Server integration, Home Assistant long-lived access token, Ned entity map at `references/home-assistant-entity-map.md`, optional `mcp-proxy` fallback only if the installed Hermes/MCP runtime cannot speak Streamable HTTP directly. Community `ha-mcp` / `ha-mcp-server` are deferred options, not the default.

---

## Current Known State

- Ned repo canonical path: `/Users/neimaseirafi/Documents/ned`
- Home Assistant entity map: `references/home-assistant-entity-map.md`
- Home Assistant local URL: `http://homeassistant.local:8123`
- Home Assistant official MCP endpoint: `http://homeassistant.local:8123/api/mcp`
  - unauthenticated probe returns HTTP 401, confirming the server integration is installed and auth-gated.
- Hermes MCP support: available; Hermes config uses `url:` for remote HTTP/SSE/StreamableHTTP MCP servers.
- Hermes MCP server configured: `homeassistant` using native HTTP / Streamable HTTP.
- `mcp-proxy`: not used; keep only as fallback if native HTTP ever regresses.
- Official HA MCP tools discovered: 20 total; see `references/ha-mcp-setup.md` for the exact list and safety notes.
- Read-only validation: passed via `GetLiveContext` in a fresh Hermes CLI session.
- Entity-map comparison: completed on 2026-05-29; `references/home-assistant-entity-map.md` now records MCP live-state differences while staying curated.
- First safe write test: completed with explicit approval; `HassLightSet` turned on Family Room Main Lights to ~30%, but area-based Assist targeting also affected nearby Family Room lights. Future writes should use narrower selectors or an allowlisted wrapper.
- Usability gap: Home Assistant is currently more of a project backend than a useful daily control surface. Roadmap now includes a human-facing pass: Companion App, mobile dashboard, scenes, and practical automations before deeper expansion.
- Home Assistant VM boot reliability remains separate work; do not confuse MCP readiness with boot reliability.

## Security Boundary

The first successful milestone is **read-only state access**, not full control.

Do not start with:

- locks
- cameras/security
- HVAC
- config mutation
- automation editing
- unbounded Sonos volume
- arbitrary Home Assistant service calls as a casual default

Initial safe write scope, after read-only validation:

- lights on/off
- brightness/color for mapped Hue lights
- scenes
- bounded media pause/resume or volume, with explicit limits

### Official MCP Server read-only reality

The official integration has no per-entity "read-only but block writes" mode. Its access model is:

1. **Control Home Assistant** option ON/OFF — coarse: either clients can act, or they cannot.
2. **Exposed Entities** page — which entities are visible at all.

For the genuinely read-only first session, set **Control Home Assistant OFF**. That is stronger than policy-by-instruction and avoids needing a custom wrapper just to achieve safe read-only. Flip it ON only when Phase 8 reaches the first approved write test.

Suggested Sonos safety policy:

```text
Never set Sonos volume above 35% unless Neima explicitly asks in that turn.
```

---

## Time Estimate Summary

Total expected hands-on installation/validation time:

```text
140–225 minutes total
≈ 2h20m–3h45m
```

Practical planning estimate:

```text
One focused evening if everything works.
Two sessions if we hit MCP tool-scope or token/config issues.
```

Per-phase estimates:

- Phase 0 — Safety framing: 10–15 min
- Phase 1 — Create HA token: 5–10 min
- Phase 1.5 — Create dedicated HA identity: 10–15 min
- Phase 2 — Install/configure official HA MCP Server strategy: 15–20 min
- Phase 3 — Add Hermes MCP config: 10–20 min
- Phase 4 — Restart gateway and test MCP connection: 10–15 min
- Phase 5 — Tool discovery and risk review: 15–25 min
- Phase 6 — Read-only validation: 20–30 min
- Phase 7 — Compare live state against entity map: 20–35 min
- Phase 8 — First safe write test: 15–25 min
- Phase 9 — Document results back into Ned: 15–25 min

---

## Phase 0: Safety Framing

**Required time:** 10–15 minutes

**Objective:** Agree that the first MCP milestone is read-only Home Assistant awareness.

**Files:**

- Read: `references/home-assistant-entity-map.md`
- Read: `memory/project_homelab_roadmap.md`
- Modify later: this plan as results are discovered

**Steps:**

1. Read the current entity map.
2. Confirm initial allowed questions:
   - What lights are on?
   - What devices are unavailable?
   - What media players are active?
   - Is WAN connected?
   - Summarize the house by room.
3. Confirm initial blocked actions:
   - lock/security/camera changes
   - HVAC changes
   - arbitrary automation/config edits
   - broad `call_service` use without explicit approval

**Verification:** The operator can state exactly what Hermes is allowed to do before any token is wired in.

---

## Phase 1: Create Home Assistant Long-Lived Token

**Required time:** 5–10 minutes

**Objective:** Create a Home Assistant token for Hermes MCP access without committing secrets to Git. Prefer a dedicated `Hermes MCP` Home Assistant user rather than Neima's admin account; Phase 1.5 formalizes that identity split.

**Files:**

- Modify locally only: `~/.hermes/.env`
- Do not commit: tokens, secrets, generated auth dumps

**Steps:**

1. In Home Assistant, create or switch to the dedicated `Hermes MCP` user from Phase 1.5 when possible.
2. Go to that user profile.
3. Scroll to **Long-Lived Access Tokens**.
4. Create a token named:

```text
Hermes HA MCP
```

5. Store it in `~/.hermes/.env`:

```bash
HA_MCP_URL=http://homeassistant.local:8123
HA_MCP_TOKEN=[REDACTED]
HA_MCP_TIMEZONE=America/Chicago
```

**Verification:** `~/.hermes/.env` contains the three variable names above, the token belongs to the dedicated `Hermes MCP` user if possible, and no token appears in the Ned repo.

---

## Phase 1.5: Create a Dedicated Low-Privilege HA Identity

**Required time:** 10–15 minutes

**Objective:** Avoid using Neima's admin account's long-lived token. Create a separate `Hermes MCP` Home Assistant user so the token is independently auditable and revocable.

**Reality check on HA's permission model:** Home Assistant's per-user permissions are coarse, and non-admin token creation can be restricted depending on version. So the durable win here is **identity separation** and one-click **revocation**, not true least privilege. The actual capability constraint comes from the official integration's entity-exposure allowlist and the `Control Home Assistant` toggle in Phase 2, not from the user role.

**Steps:**

1. Create a Home Assistant user named `Hermes MCP`.
2. Give it the lowest practical role that can still authenticate and read exposed state.
3. Generate the long-lived token from that user, named `Hermes HA MCP`.
4. Store it in `~/.hermes/.env` using the `HA_MCP_*` variables from Phase 1.

**Verification:** The token belongs to the `Hermes MCP` user, not Neima's admin account, and can be revoked without touching admin access.

---

## Phase 2: Choose MCP Server Strategy

**Required time:** 15–20 minutes

**Objective:** Install/configure the official Home Assistant MCP Server integration first, with Home Assistant itself acting as the MCP server and entity exposure serving as the structural allowlist.

**Recommended first server:**

```text
Official Home Assistant "Model Context Protocol Server" integration
```

Use it for:

- live entity discovery
- state queries
- read-only validation with `Control Home Assistant` OFF
- later tightly scoped writes by enabling control and exposing only deliberate entities

**Do not confuse these implementations:**

1. **Model Context Protocol Server** — correct first target. Installed in HA. HA serves `/api/mcp` over Streamable HTTP.
2. **Model Context Protocol** — reverse direction. HA consumes other MCP servers. Not this project.
3. **ha-mcp** — community REST/WebSocket package with structural write power. Defer.

Potential follow-up servers/packages:

```text
ha-mcp
ha-mcp-server
custom Ned/HA wrapper
```

Use them only for a specific need after official read-only value is proven.

**Decision rule:**

Prefer the official MCP Server integration first, because entity exposure IS the allowlist — no custom wrapper required for first-session read-only when `Control Home Assistant` is OFF. Expose a minimal read set, validate, then expand exposure deliberately.

Only reach for `ha-mcp` (REST/WebSocket, structural writes) once read-only value is proven AND a specific structural need exists. If `ha-mcp` exposes read and write through one generic tool with no exposure gating, it does NOT get persistent write access until a custom read-only wrapper or a tight allowlist is in place.

**Verification:** Record the official integration settings, exposed entity set, and control-toggle state in this plan or a future `references/ha-mcp-setup.md`.

---

## Phase 3: Add Hermes MCP Config

**Required time:** 10–20 minutes

**Objective:** Configure Hermes native MCP client to connect to Home Assistant's official Streamable HTTP MCP endpoint.

**Files:**

- Modify: `~/.hermes/config.yaml`
- Read: `~/.hermes/.env`
- Do not modify: Ned repo secrets

**Verified Home Assistant official MCP Server facts:**

```text
Endpoint:   http://homeassistant.local:8123/api/mcp   (NOT /mcp)
Transport:  Streamable HTTP, stateless. The integration is NOT a stdio npx package.
Introduced: HA 2025.2; current HAOS is well past this.
Install:    Settings > Devices & Services > Add Integration > "Model Context Protocol Server".
Auth:       OAuth (IndieAuth) OR a Long-Lived Access Token sent as a Bearer header.
Control:    "Control Home Assistant" option governs whether clients can act at all.
Exposure:   Clients can only see/control entities exposed via the Exposed Entities page.
```

**Hermes-native HTTP config:**

Hermes supports remote HTTP/SSE/StreamableHTTP MCP servers via the `url:` config key. Use this as the default if the installed Hermes runtime has the MCP Python package with Streamable HTTP support:

```yaml
mcp_servers:
  homeassistant:
    url: "http://homeassistant.local:8123/api/mcp"
    headers:
      Authorization: "Bearer ${HA_MCP_TOKEN}"
    timeout: 120
    connect_timeout: 60
```

Before trusting this block, confirm the active Hermes environment has MCP Streamable HTTP support:

```bash
python3 - <<'PY'
import mcp.client.streamable_http
print("streamable_http available")
PY
```

If that import fails, install/upgrade the MCP SDK in the Hermes runtime, then restart Hermes:

```bash
pip install --upgrade mcp
```

**Fallback bridge if HTTP transport is unavailable:**

If Hermes' current MCP runtime cannot speak Streamable HTTP directly, use `mcp-proxy` as a stdio bridge. `uv` is already available on the Mac Mini:

```bash
uv tool install git+https://github.com/sparfenyuk/mcp-proxy
```

```yaml
mcp_servers:
  homeassistant:
    command: "mcp-proxy"
    args:
      - "--transport=streamablehttp"
      - "--stateless"
      - "http://homeassistant.local:8123/api/mcp"
    env:
      API_ACCESS_TOKEN: "${HA_MCP_TOKEN}"
    timeout: 120
    connect_timeout: 60
```

**Deferred community lights/scenes server config, if ever used:**

Standardize local secret names on `HA_MCP_*`, then map them into whatever names the specific server README requires. Example only — verify the package README before trusting it:

```yaml
mcp_servers:
  ha_lights:
    command: "npx"
    args: ["-y", "ha-mcp-server"]
    env:
      HA_URL: "${HA_MCP_URL}"
      HA_TOKEN: "${HA_MCP_TOKEN}"
    timeout: 120
    connect_timeout: 60
```

**Verification:** Run:

```bash
hermes mcp list
```

Expected before restart: server is listed in config, but tools may not be active until Hermes restarts.

---

## Phase 4: Restart Gateway and Test MCP Connection

**Required time:** 10–15 minutes

**Objective:** Restart Hermes so MCP tools are discovered at startup.

**Commands:**

```bash
hermes gateway restart
hermes mcp list
hermes mcp test homeassistant
```

If testing fails, inspect logs:

```bash
grep -i "mcp\|homeassistant\|home assistant" ~/.hermes/logs/gateway.log | tail -80
```

Troubleshooting anchors from the official HA docs:

```text
404 at /api/mcp  -> the MCP Server integration is not actually configured in HA.
401 at /api/mcp  -> the long-lived access token is wrong or not being sent as Bearer auth.
```

Also verify the endpoint path is `/api/mcp`, not `/mcp`.

**Verification:** The Home Assistant MCP server appears as connected or testable, and Hermes startup logs show MCP discovery without credential leakage.

---

## Phase 5: Tool Discovery and Risk Review

**Required time:** 15–25 minutes

**Objective:** Identify exactly which MCP tools Hermes received and whether they are too broad.

**Commands:**

```bash
hermes mcp list
hermes mcp configure homeassistant
```

**What to look for:**

- Tool names prefixed like `mcp_homeassistant_*`
- Whether reads and writes are separate tools
- Whether `Control Home Assistant` is OFF for the first read-only session
- Whether one generic tool can run both `get_state` and `call_service`
- Whether high-risk services are visible despite the Exposed Entities allowlist

**Decision:**

- If read tools are separable, enable read tools first.
- If `Control Home Assistant` is OFF, treat this as the preferred first-session structural read-only boundary.
- If all actions sit behind one generic tool, keep first session read-only and do not grant persistent write access.
- If dangerous write tools are separable, disable them.

**Verification:** Write down the actual discovered tool names in `references/ha-mcp-setup.md` after the first live run.

---

## Phase 6: Read-Only Validation

**Required time:** 20–30 minutes

**Objective:** Prove Hermes can answer live Home Assistant questions accurately.

**Test prompts:**

```text
What Home Assistant entities are unavailable?
```

```text
What lights are currently on?
```

```text
What media players are active?
```

```text
Summarize the house by room using the Ned entity map as context.
```

**Expected comparison anchors from the static entity map:**

- `light.listening_room_lamp` was previously unavailable.
- `media_player.65_oled` was previously unavailable.
- Music Assistant `_2` duplicate players may appear and should be treated carefully.
- Family Room lights/TV lightstrip were on when the entity map was generated, but live state may differ.

**Verification:** Hermes can distinguish static map facts from live state facts and can cite which state came from Home Assistant now.

---

## Phase 7: Compare Live State Against Entity Map

**Status:** Complete as of 2026-05-29. The entity map was refreshed from a read-only `GetLiveContext` comparison without turning it into a raw entity dump.

**Required time:** 20–35 minutes

**Objective:** Use MCP data to improve the curated entity map without expanding it into noise.

**Files:**

- Read/modify: `references/home-assistant-entity-map.md`
- Create/modify: `references/ha-mcp-setup.md`

**Compare:**

1. Entities in HA but missing from the map.
2. Entities in the map but unavailable/stale.
3. Rooms with unclear naming.
4. Duplicate Music Assistant entities.
5. Entities agents should intentionally ignore.

**Do not over-expand:**

Keep the entity map curated. Agents need a control surface, not every backup sensor and integration artifact.

**Verification:** The entity map has fewer contradictions and still remains readable by an agent.

---

## Phase 7.5: Human-Facing Home Assistant Usability Pass

**Status:** Added after Neima called out the core problem: Home Assistant is not yet useful compared to Google Home or Apple Home.

**Objective:** Turn Home Assistant from an agent/MCP backend into something Neima would actually use day-to-day.

**Files:**

- Read/modify: `references/home-assistant-entity-map.md`
- Create/modify if needed: `references/ha-usability-notes.md`
- Modify if needed: `memory/project_homelab_roadmap.md`

**Scope:**

1. Companion App setup:
   - install Home Assistant Companion App on Neima's phone
   - confirm remote/local URL behavior
   - enable useful permissions only: notifications, location if wanted for presence, local network/Bluetooth if needed
   - confirm phone appears as a tracked device/sensor set in HA
2. Existing automation/source-app inventory:
   - inventory current routines/automations/scenes from Google Home, Lutron, and Hue before recreating anything
   - classify each item as: migrate to HA, leave in source app temporarily, delete/replace, or defer
   - record trigger, conditions, target devices, expected behavior, and why the automation exists
   - avoid duplicate automations fighting each other across Google Home / Lutron / Hue / HA during the transition
3. Mobile dashboard:
   - create a simple phone-first dashboard for actually used rooms
   - surface common controls instead of raw entity sprawl
   - prioritize Family Room, Entryway, Kitchen/Dining, Master Bedroom, Sonos, and any "all off" controls
4. Scenes:
   - recreate useful Lutron/Hue/Google scenes in HA first, then add new HA-native scenes only where they improve daily use
   - first pass lighting scenes for common modes, e.g. Family Room normal/movie/off, Entryway evening/off, Kitchen/Dining dinner/off, Master Bedroom night/off
   - prefer scene activation over broad ad-hoc natural-language service calls when agents act
5. Automations:
   - migrate useful source-app automations into HA when HA can be the more reliable owner
   - start with convenience automations that are visibly better than Google Home / Apple Home
   - avoid clever but annoying automations; every automation needs an obvious manual override
   - likely starters: sunset/evening lighting, bedtime/all-off, simple presence-aware notifications, and low-risk Sonos/media convenience
6. Agent integration:
   - expose scenes/scripts to MCP as safer action targets
   - keep locks/security/HVAC/cameras out of casual automation until explicitly planned

**Verification:** Neima can open the HA app and do common house actions faster or better than before; at least one scene and one automation are useful without needing Hermes in the loop.

---

## Phase 8: First Safe Write Test

**Status:** Complete as of 2026-05-29 with explicit approval. Result succeeded, but revealed that official MCP natural-language targeting can affect an area when `area` is included alongside a named light.

**Required time:** 15–25 minutes

**Objective:** Perform one low-risk write only after read-only validation succeeds.

**Candidate tests:**

```text
Turn off the Family Room TV lightstrip.
```

Target:

```text
light.tv_lightstrip
```

Or:

```text
Activate Entryway Relax.
```

Target:

```text
scene.entryway_relax
```

**Rules:**

- Ask Neima before the first write.
- Run the first write only after a fully clean read-only session.
- The first write target must be a device physically visible to Neima in the same room, so the result is verified by eye, not just by state.
- Use one obvious target entity.
- Verify state afterward.
- Do not test broad service calls.

**Verification:** Home Assistant confirms the target state changed and no unrelated entities changed.

**Actual result:** `light.family_room_main_lights` changed to on at raw brightness 76 (~30%), but the broader Family Room light area also moved to roughly 30% because the MCP call included `area="Family Room"`. Treat this as a safety lesson: prefer exact/narrow selectors, and consider a custom allowlisted wrapper for deterministic entity-only writes.

---

## Phase 9: Document Results Back Into Ned

**Required time:** 15–25 minutes

**Objective:** Make Claude and Hermes share the same updated operational knowledge.

**Files:**

- Create: `references/ha-mcp-setup.md`
- Modify if needed: `references/home-assistant-entity-map.md`
- Modify if needed: `memory/project_homelab_roadmap.md`
- Modify if needed: `memory/project_ai_learning.md`

**Record:**

- MCP integration/transport used, including whether Hermes native HTTP or `mcp-proxy` fallback was chosen
- exact Hermes config shape, with tokens redacted
- discovered tool names
- read-only tests passed/failed
- first write test passed/failed, if performed
- unsafe capabilities intentionally blocked or deferred
- cleanup list

**Verification:** Git diff contains docs and curated facts only; no secrets.

---

## Success Criteria

The HA MCP project is considered successful when:

1. Hermes can query live Home Assistant state through MCP.
2. Hermes can answer “what lights are on?” using live state, not stale markdown.
3. Hermes can identify unavailable mapped entities.
4. Hermes can compare live HA state to `references/home-assistant-entity-map.md`.
5. First write, if approved, is limited to one light/scene and verified afterward.
6. Home Assistant has a phone-first control surface Neima would actually use.
7. Existing Google Home, Lutron, and Hue automations/scenes are inventoried, with each item either migrated, intentionally left in place, replaced, or deferred.
8. At least one scene and one automation provide real daily value beyond Google Home / Apple Home.
9. The final setup is documented in Ned with secrets redacted.

## Deferral Criteria

Pause and reassess if:

- HA token appears in Git diff.
- MCP server exposes only a broad unrestricted action tool and no safe read-only separation.
- Home Assistant VM is unstable after reboot.
- Home Assistant cannot be reached reliably at `homeassistant.local:8123`.
- Tool discovery adds too many risky capabilities with no way to disable them.

## Long-Term Direction

The likely durable architecture is:

1. Official HA MCP Server integration for read-only state with `Control Home Assistant` OFF.
2. Human-facing Home Assistant usefulness: Companion App, phone-first dashboard, and migration inventory from Google Home / Lutron / Hue.
3. HA-owned scenes and practical automations, with source-app duplicates disabled only after verification.
4. Official HA MCP Server integration with narrow exposed entities for safe writes, or a lights/scenes-only MCP wrapper if the discovered tools are too broad.
5. Custom Ned MCP for project/homelab coaching context.
6. Hermes cron health agent for daily status summaries.
7. Optional Home Assistant automations that agents can trigger indirectly through pre-approved scripts/scenes rather than arbitrary service calls.
