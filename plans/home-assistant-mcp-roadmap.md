# Home Assistant MCP Roadmap

> **For Claude / Hermes:** This is the shared implementation roadmap for bringing Home Assistant into the agentic workflow. Treat the first session as read-only unless Neima explicitly approves a write test.

**Goal:** Connect Hermes to Home Assistant through MCP so agents can read live smart-home state, compare it against the curated entity map, and later perform tightly scoped safe controls.

**Architecture:** Start with a generic Home Assistant MCP server for live state discovery and read-only validation. Add or switch to a lights/scenes-only MCP server for safer writes. If the generic server exposes too much power behind one tool, build a small custom read-only wrapper before granting broad agent access.

**Tech Stack:** Hermes Agent native MCP client, Home Assistant long-lived access token, Node/npx MCP servers, `ha-mcp`, optionally `ha-mcp-server`, Ned entity map at `references/home-assistant-entity-map.md`.

---

## Current Known State

- Ned repo canonical path: `/Users/neimaseirafi/Documents/ned`
- Home Assistant entity map: `references/home-assistant-entity-map.md`
- Home Assistant local URL: `http://homeassistant.local:8123`
- Hermes MCP support: available
- Node/npx: available on the Mac Mini
- uv: available on the Mac Mini
- Existing Hermes MCP servers before this plan: none configured
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

Suggested Sonos safety policy:

```text
Never set Sonos volume above 35% unless Neima explicitly asks in that turn.
```

---

## Time Estimate Summary

Total expected hands-on installation/validation time:

```text
130–210 minutes total
≈ 2h10m–3h30m
```

Practical planning estimate:

```text
One focused evening if everything works.
Two sessions if we hit MCP tool-scope or token/config issues.
```

Per-phase estimates:

- Phase 0 — Safety framing: 10–15 min
- Phase 1 — Create HA token: 5–10 min
- Phase 2 — Choose MCP server strategy: 10–15 min
- Phase 3 — Add Hermes MCP config: 10–15 min
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

**Objective:** Create a Home Assistant token for Hermes MCP access without committing secrets to Git.

**Files:**

- Modify locally only: `~/.hermes/.env`
- Do not commit: tokens, secrets, generated auth dumps

**Steps:**

1. In Home Assistant, go to Neima's user profile.
2. Scroll to **Long-Lived Access Tokens**.
3. Create a token named:

```text
Hermes HA MCP
```

4. Store it in `~/.hermes/.env`:

```bash
HA_MCP_URL=http://homeassistant.local:8123
HA_MCP_TOKEN=[REDACTED]
HA_MCP_TIMEZONE=America/Chicago
```

**Verification:** `~/.hermes/.env` contains the three variable names above, and no token appears in the Ned repo.

---

## Phase 2: Choose MCP Server Strategy

**Required time:** 10–15 minutes

**Objective:** Choose the starting MCP server and define when to add a safer wrapper.

**Recommended first server:**

```text
ha-mcp
```

Use it for:

- live entity discovery
- state queries
- service visibility
- initial read-only validation

Potential follow-up server:

```text
ha-mcp-server
```

Use it for safer writes limited to:

- lights
- scenes

**Decision rule:**

If `ha-mcp` exposes read and write through one generic tool/action schema, then treat it as read-only by policy during the first session. If that boundary feels too loose, build a custom read-only MCP wrapper before giving Hermes persistent Home Assistant access.

**Verification:** Record which package is selected and why in this plan or a future `references/ha-mcp-setup.md`.

---

## Phase 3: Add Hermes MCP Config

**Required time:** 10–15 minutes

**Objective:** Configure Hermes native MCP client to launch the Home Assistant MCP server.

**Files:**

- Modify: `~/.hermes/config.yaml`
- Read: `~/.hermes/.env`
- Do not modify: Ned repo secrets

**Generic HA MCP config:**

```yaml
mcp_servers:
  homeassistant:
    command: "npx"
    args: ["-y", "ha-mcp"]
    env:
      HA_MCP_URL: "${HA_MCP_URL}"
      HA_MCP_TOKEN: "${HA_MCP_TOKEN}"
      HA_MCP_TIMEZONE: "${HA_MCP_TIMEZONE}"
    timeout: 120
    connect_timeout: 60
```

**Optional lights/scenes server config:**

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
- Whether one generic tool can run both `get_state` and `call_service`
- Whether high-risk services are visible

**Decision:**

- If read tools are separable, enable read tools first.
- If all actions sit behind one generic tool, keep first session read-only by instruction and consider a custom wrapper.
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

## Phase 8: First Safe Write Test

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
- Use one obvious target entity.
- Verify state afterward.
- Do not test broad service calls.

**Verification:** Home Assistant confirms the target state changed and no unrelated entities changed.

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

- MCP package used
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
6. The final setup is documented in Ned with secrets redacted.

## Deferral Criteria

Pause and reassess if:

- HA token appears in Git diff.
- MCP server exposes only a broad unrestricted action tool and no safe read-only separation.
- Home Assistant VM is unstable after reboot.
- Home Assistant cannot be reached reliably at `homeassistant.local:8123`.
- Tool discovery adds too many risky capabilities with no way to disable them.

## Long-Term Direction

The likely durable architecture is:

1. Generic HA MCP or custom wrapper for read-only state.
2. Lights/scenes-only MCP for safe writes.
3. Custom Ned MCP for project/homelab coaching context.
4. Hermes cron health agent for daily status summaries.
5. Optional Home Assistant automations that agents can trigger indirectly through pre-approved scripts/scenes rather than arbitrary service calls.
