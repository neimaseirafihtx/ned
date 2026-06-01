# Home Assistant Usability Pass

**Created:** 2026-06-01  
**Owner:** Neima / Ned  
**Status:** Active — first-pass design and inventory scaffold

---

## Goal

Make Home Assistant useful for humans day-to-day, not just useful for agents.

Success means:

- Neima can open the HA Companion App and use it faster than Google Home / Apple Home for common controls.
- The first dashboard is room/mode oriented, not a raw entity dump.
- Existing Google Home, Hue, and Lutron routines are inventoried before recreating anything.
- Useful scenes/scripts exist in HA as exact, safe control targets.
- Source-app duplicate automations are disabled only after HA replacements are tested.

---

## Current Known HA Control Surface

Source: `references/home-assistant-entity-map.md` plus live HA REST state check on 2026-06-01.

### First-pass useful rooms

| Room / Area | Entities | Notes |
|---|---|---|
| Family Room | `light.family_room`, `light.family_room_lamp`, `light.tv_lightstrip`, `light.family_room_main_lights`, `media_player.living_room`, `media_player.75_the_frame` | Highest-value first room. Important: “Family Room lights” spans Hue + Lutron, not just the Hue group. |
| Kitchen / Dining | `light.kitchen_main_lights`, `light.kitchen_island_pendants`, `light.dining_room_main_lights` | Good second room group; likely useful for evening/dinner scenes. |
| Entryway | `light.entryway`, `light.entry_lamp`, `scene.entryway_relax`, `scene.entryway_bright_80` | Existing Hue scenes already available. |
| Master Bedroom / Neima’s Room | `light.master_bedroom_main_lights`, `media_player.neimas_room` | Keep simple at first. |
| Listening Room | `light.listening_room`, Hue scenes, `media_player.listening_room` | Useful but not first-pass daily dashboard unless Neima uses it often. |

### Existing HA scenes discovered

| Scene | Friendly name | Source / Notes | First-pass decision |
|---|---|---|---|
| `scene.family_room_dimmed` | Family Room Dimmed | Hue scene, brightness target 65 | Use as ingredient, but it does not include Lutron main lights. |
| `scene.entryway_relax` | Entryway Relax | Hue scene, brightness target 143 | Keep; expose on dashboard. |
| `scene.entryway_bright_80` | Entryway Bright 80% | Hue scene, brightness target 205 | Keep; expose if useful. |
| `scene.listening_room_read` | Listening Room Read | Hue scene, brightness target 255 | Keep for later. |
| `scene.listening_room_relax` | Listening Room Relax | Hue scene, brightness target 143 | Keep for later. |
| `scene.listening_room_warm_embrace` | Listening Room Warm Embrace | Hue scene, brightness target 102 | Keep for later. |
| `scene.listening_room_sleepy` | Listening Room Sleepy | Hue scene, brightness target 64 | Keep for later. |
| `scene.smart_bridge_2_all_second_floor` | Smart Bridge 2 All Second Floor | Lutron scene; broad scope | Do not expose to agents casually. Review manually before use. |

### Existing automations discovered from HA API snapshot

| Entity | Friendly name | Source | Current decision |
|---|---|---|---|
| `switch.hue_bridge_automation_evening_lamps` | Evening Lamps automation | Hue Bridge automation exposed to HA API snapshot | Inventory before recreating; likely migrate/replace in HA later. |
| `switch.hue_bridge_automation_morning_lamp` | Morning Lamp automation | Hue Bridge automation exposed to HA API snapshot | Inventory before recreating; likely migrate/replace in HA later. |

Live REST check on 2026-06-01 did not show HA-native `automation.*` or `script.*` entities. That means the first pass is likely starting from vendor-app scenes/automations plus HA-integrated device entities, not from an existing HA automation library.

---

## First Mobile Dashboard Design

Working name: `Home`

Design principle: 4 room cards + a small status/quick-actions area. No entity sprawl.

### Top quick actions

| Button | Purpose | Backing target |
|---|---|---|
| All common lights off | One-tap shutdown for common spaces | New exact HA script, not broad area targeting |
| Family Room Relax | Comfortable evening TV/lounge state | New exact HA script/scene combining Hue + Lutron |
| Movie Mode | TV-focused dim/off pattern | New exact HA script/scene combining Hue + Lutron |
| Night / Shutdown | Later: broader evening shutdown | Defer until inventory confirms what should be included |

### Room cards

#### Family Room

Show:

- `light.family_room_main_lights`
- `light.family_room_lamp`
- `light.tv_lightstrip`
- `media_player.living_room`
- `media_player.75_the_frame`

Actions:

- Family Room Relax
- Movie Mode
- Family Room Off

#### Kitchen / Dining

Show:

- `light.kitchen_main_lights`
- `light.kitchen_island_pendants`
- `light.dining_room_main_lights`

Actions:

- Kitchen / Dining Bright
- Kitchen / Dining Evening
- Kitchen / Dining Off

#### Entryway

Show:

- `light.entryway`
- `light.entry_lamp`

Actions:

- Entryway Relax
- Entryway Bright 80%
- Entryway Off

#### Master Bedroom / Neima’s Room

Show:

- `light.master_bedroom_main_lights`
- `media_player.neimas_room`

Actions:

- Bedroom Off
- Bedroom Relax later if needed

---

## First Exact HA Scripts / Scenes to Create

Do not use broad natural-language/area targeting. Use exact entities.

### `script.family_room_off`

Turns off:

- `light.family_room`
- `light.family_room_lamp`
- `light.tv_lightstrip`
- `light.family_room_main_lights`

### `script.family_room_relax`

Proposed first draft:

- `light.family_room_main_lights`: on, brightness ~30–35%
- `light.family_room_lamp`: on, warm/relax if color temp available, brightness ~45–55%
- `light.tv_lightstrip`: on, low/warm or existing Hue relaxed state, brightness ~25–35%
- Avoid TV/media changes for v1.

### `script.movie_mode`

Proposed first draft:

- `light.family_room_main_lights`: off or very low, depending Neima preference
- `light.family_room_lamp`: off or low
- `light.tv_lightstrip`: on low
- Avoid TV/media changes for v1.

### `script.kitchen_dining_off`

Turns off:

- `light.kitchen_main_lights`
- `light.kitchen_island_pendants`
- `light.dining_room_main_lights`

### `script.common_lights_off`

Turns off first-pass common area lights:

- Family Room exact set
- Kitchen / Dining exact set
- Entryway exact set

Do not include bedrooms, exterior, garage, security, HVAC, locks, or cameras in v1.

---

## Migration Inventory Process

For each source app — Google Home, Hue, Lutron — record current routines/scenes before changing anything.

Decision labels:

- **Migrate** — HA should own it.
- **Leave** — source app stays owner for now.
- **Replace** — recreate in HA with improved logic.
- **Delete** — stale or unwanted.
- **Defer** — useful, but not first pass.

Inventory doc:

- `references/home-assistant-automation-inventory.md`

---

## Safe Rollout Order

1. Finish inventory from Google Home, Hue, and Lutron.
2. Create HA scripts/scenes manually or via exact YAML after review.
3. Test each script manually from HA.
4. Add dashboard buttons.
5. Disable matching source-app automation only after the HA version works.
6. Keep a rollback note: re-enable source-app automation if HA version behaves poorly.

---

## Current Status

- [x] Entity map exists.
- [x] HA API token works for read-state checks.
- [x] First-pass dashboard target rooms identified.
- [x] First exact script/scene candidates identified.
- [ ] Companion App installed/configured on Neima's phone.
- [ ] Google Home routines inventoried.
- [ ] Hue scenes/automations inventoried from app.
- [ ] Lutron scenes/schedules inventoried from app.
- [ ] First HA scripts created.
- [ ] First HA dashboard created.
- [ ] Source-app duplicate automation disabled after HA replacement is tested.
