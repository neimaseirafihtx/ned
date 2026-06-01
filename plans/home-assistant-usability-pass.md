# Home Assistant Usability Pass

**Created:** 2026-06-01  
**Owner:** Neima / Ned  
**Status:** Active — `Neima Home` dashboard created with Family Room script buttons for Evening/Movie

---

## Goal

Make Home Assistant useful for humans day-to-day, not just useful for agents.

Success means:

- Neima can open the HA Companion App and use it faster than Google Home / Apple Home for common controls.
- The first dashboard is room/mode oriented, not a raw entity dump.
- Existing Apple Home, Google Home, Hue, and Lutron routines are inventoried before recreating anything.
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
| `scene.family_room_evening` | Family Room Evening | HA scene created 2026-06-01 from Apple Home Evening values; corrected to flattened scene attributes after initial test issue; later hidden from UI because the Family Room area scene trigger did not drive lights while the script worked | Do not expose as the primary dashboard control; use `script.family_room_evening`. |
| `scene.family_room_movie` | Family Room Movie | HA scene created 2026-06-01 from Apple Home Movie values; corrected to flattened scene attributes after initial test issue; later hidden from UI because the Family Room area scene trigger did not drive lights while the script worked | Do not expose as the primary dashboard control; use `script.family_room_movie`. |
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

Working name: `Neima Home`

Live HA dashboard created 2026-06-01:

- Dashboard title: `Neima Home`
- URL path: `/neima-home/home`
- Sidebar: shown
- Previous `/ned-home/home` dashboard path is hidden from the sidebar as an old-path rollback copy.
- First button grid: `Family Room Modes`
- Buttons call `script.turn_on` directly:
  - `script.family_room_evening`
  - `script.family_room_movie`
- Room/status cards currently included:
  - `Family Room`
  - `Kitchen / Dining`
  - `Entryway`
  - `Neima’s Room`
  - `Listening Room`
  - `Guestroom`
  - `Office / Garage`
  - `Exterior`
- Reason: the Family Room area page's auto `Scenes > Dimmed`/scene-trigger path did not drive the physical lights, while Developer Tools `script.turn_on` worked. Use explicit script buttons for daily controls.

Design principle: 4 room cards + a small status/quick-actions area. No entity sprawl.

### Top quick actions

| Button | Purpose | Backing target |
|---|---|---|
| Evening | Existing daily Apple Home scene translated into HA | `script.family_room_evening` combining Hue + Lutron; prefer script over scene trigger |
| Movie Mode | Existing Apple Home movie scene translated into HA | `script.family_room_movie` combining Hue + Lutron; prefer script over scene trigger |
| All common lights off | One-tap shutdown for common spaces | New exact HA script, not broad area targeting |
| Entryway Relax / Bright | Existing Hue scenes surfaced in HA | Existing HA scene entities |

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

## Captured Source-App Inventory

Source file from Neima:

```text
references/smart_home_inventory.md
```

Summary:

| Source | Item | Decision | Notes |
|---|---|---|---|
| Apple Home | Evening scene | Migrate first | Best first HA scene; spans Kitchen, Family/Living, Dining, Hue, and Lutron. |
| Apple Home | Movie scene | Migrate second | Best second HA scene; clear exact lighting behavior. |
| Google Home | All Lights Off at 11:00 PM | Replace later | First build/test exact `script.common_lights_off`; schedule only after target list is approved. |
| Hue | Morning Lamp 7–9 AM | Defer / maybe leave | Entryway only; low priority. |
| Hue | Evening Lamps 5–11 PM | Leave for now, maybe replace later | Reliable vendor automation; do not disable until HA Evening is proven. |
| Lutron | Outdoor Lights at sunset | Leave | Exterior/safety-ish and reliable in Lutron. |
| Lutron | Outdoor Lights Off at 11:30 PM | Leave | Exterior/safety-ish and reliable in Lutron. |

---

## First Exact HA Scripts / Scenes to Create

Do not use broad natural-language/area targeting. Use exact entities.

### `scene.family_room_evening` / `script.family_room_evening`

Exact translation target from Apple Home `Evening`:

- `light.kitchen_island_pendants`: on, brightness 30%
- `light.kitchen_main_lights`: off
- `light.tv_lightstrip`: on, brightness 28%
- `light.family_room_lamp`: on, brightness 75%
- `light.family_room_main_lights`: on, brightness 1%
- `light.dining_room_main_lights`: on, brightness 20%

Resolved: Neima confirmed Apple Home `Evening` should set the TV lightstrip to 28% brightness.

### `scene.family_room_movie` / `script.family_room_movie`

Exact translation target from Apple Home `Movie`:

- `light.kitchen_island_pendants`: on, brightness 35%
- `light.tv_lightstrip`: on, brightness 19%
- `light.family_room_lamp`: on, brightness 25%
- `light.family_room_main_lights`: off
- `light.dining_room_main_lights`: off

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

### `script.movie_mode_legacy_draft`

Superseded by the exact Apple Home `Movie` translation above. Keep only as historical idea; do not build this version.

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
4. Add dashboard buttons or area-page controls that call `script.turn_on`; do not rely on the auto-generated area scene trigger for mixed Hue + Lutron scenes.
5. Disable matching source-app automation only after the HA version works.
6. Keep a rollback note: re-enable source-app automation if HA version behaves poorly.

---

## Current Status

- [x] Entity map exists.
- [x] HA API token works for read-state checks.
- [x] First-pass dashboard target rooms identified.
- [x] First exact script/scene candidates identified.
- [x] Apple Home Evening/Movie scenes inventoried.
- [x] Google Home All Lights Off automation inventoried.
- [x] Hue Morning Lamp and Evening Lamps automations inventoried.
- [x] Lutron outdoor schedules inventoried.
- [ ] Companion App installed/configured on Neima's phone.
- [x] Google Home routines inventoried, first pass.
- [x] Hue scenes/automations inventoried from app, first pass.
- [x] Lutron scenes/schedules inventoried from app, first pass.
- [x] Neima approved exact HA script creation.
- [x] First HA scripts created.
- [x] First HA scripts tested manually from Developer Tools; Neima confirmed `script.turn_on` worked.
- [x] Family Room area metadata corrected: `script.family_room_evening` and `script.family_room_movie` assigned to the `family_room` area; corresponding scene entities hidden from UI to prevent the non-working scene-trigger path.
- [x] First HA dashboard created: `Neima Home`, with `Family Room Modes` buttons wired to `script.turn_on`; expanded with room/status cards for Family Room, Kitchen/Dining, Entryway, Neima’s Room, Listening Room, Guestroom, Office/Garage, and Exterior.
- [ ] Source-app duplicate automation disabled after HA replacement is tested.
