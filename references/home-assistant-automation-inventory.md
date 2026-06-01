# Home Assistant Automation / Scene Inventory

**Created:** 2026-06-01  
**Updated:** 2026-06-01 from `references/smart_home_inventory.md`  
**Purpose:** Inventory existing Apple Home, Google Home, Hue, and Lutron routines before recreating anything in Home Assistant.

Do not disable or delete source-app automations until the HA replacement has been created, tested, and accepted.

---

## Decision Labels

| Label | Meaning |
|---|---|
| Migrate | Recreate in HA and eventually make HA the owner. |
| Leave | Keep in the source app for now. |
| Replace | Build a better HA-native version instead of copying exactly. |
| Delete | Stale / unwanted / duplicate. |
| Defer | Useful, but not part of first pass. |

---

## Key Takeaways

1. **Apple Home already has the two most useful scene definitions:** `Evening` and `Movie`.
2. **Google Home has a simple nightly all-lights-off automation at 11:00 PM.** This is a good HA migration candidate, but should be recreated as an exact script/automation rather than broad area targeting.
3. **Hue owns Entryway / Family Room Hue / Listening Room timed ambience.** The Hue `Evening Lamps` automation overlaps with Apple Home's Evening/Movie intent but does not include Lutron kitchen/dining/family main lights.
4. **Lutron owns outdoor light schedules.** These are reliable and safety-ish/exterior-facing; leave them in Lutron for now unless there is a specific reason to migrate.
5. **First HA migration should focus on scenes/scripts, not automations.** Build exact `Evening`, `Movie`, and `All Common Lights Off` scripts first; only then consider replacing timed automations.

---

## Apple Home — Scenes

### Scene: Evening

| Room | Accessory | State | HA Entity Mapping | Decision | Notes |
|---|---|---:|---|---|---|
| Kitchen | Island Pendants | 30% | `light.kitchen_island_pendants` | Migrate | Good HA scene target. |
| Kitchen | Main Lights | Off | `light.kitchen_main_lights` | Migrate | Exact off. |
| Living / Family Room | Hue Lightstrip | 28% | `light.tv_lightstrip` | Migrated | Neima confirmed Apple Home Evening uses 28% brightness. |
| Living / Family Room | Lamp | 75% | `light.family_room_lamp` | Migrate | Hue lamp. |
| Living / Family Room | Main Lights | 1% | `light.family_room_main_lights` | Migrate | Lutron main lights; very low, not fully off. |
| Dining Room | Main Lights | 20% | `light.dining_room_main_lights` | Migrate | Lutron. |

Decision: **Migrated to HA as `scene.family_room_evening` and `script.family_room_evening`.** This is the best first useful daily scene because it spans Hue + Lutron and matches real existing behavior.

### Scene: Movie

| Room | Accessory | State | HA Entity Mapping | Decision | Notes |
|---|---|---:|---|---|---|
| Kitchen | Island Pendants | 35% | `light.kitchen_island_pendants` | Migrate | Slightly brighter than Evening. |
| Living / Family Room | Hue Lightstrip | 19% | `light.tv_lightstrip` | Migrate | Low TV bias light. |
| Living / Family Room | Lamp | 25% | `light.family_room_lamp` | Migrate | Low lamp. |
| Living / Family Room | Main Lights | Off | `light.family_room_main_lights` | Migrate | Lutron main lights off. |
| Dining Room | Main Lights | Off | `light.dining_room_main_lights` | Migrate | Lutron. |

Decision: **Migrated to HA as `scene.family_room_movie` and `script.family_room_movie`.** This is the second-best dashboard button.

---

## Google Home — Automations

| Source | Name | Trigger | Targets | Behavior | Decision | Notes |
|---|---|---|---|---|---|---|
| Google Home | All Lights Off | Scheduled daily 11:00 PM | All lights | Turns off lights nightly | Replace in HA after exact target list is confirmed | Good candidate for `automation.nightly_common_lights_off`, but do not blindly include exterior/security/bedroom lights until reviewed. |

Current recommendation: do **not** migrate this first. First create/test an exact `script.common_lights_off`; then schedule that script at 11:00 PM only after Neima confirms the included lights.

---

## Philips Hue — Automations

| Source | Name | Trigger | Targets | Behavior | Decision | Notes |
|---|---|---|---|---|---|---|
| Hue | Morning Lamp | 7:00 AM–9:00 AM daily | Entryway entire room | Morning lighting for Entryway | Defer / maybe leave | Low-risk but not first-pass. Decide after dashboard works. |
| Hue | Evening Lamps | 5:00 PM–11:00 PM daily | Entryway, Family Room Hue lights, Listening Room | Entryway Relax, Family Room Dimmed, Listening Room Sleepy | Replace eventually, leave for now | Overlaps with HA Evening scene, but currently reliable. Do not disable until HA Evening/Movie/dashboard are working. |

### Hue automation settings captured

#### Morning Lamp

- Start: 7:00 AM
- End: 9:00 AM
- Repeat: every day
- Randomize times: no
- Selected lights:
  - Entryway — Entire Room

#### Evening Lamps

- Start: 5:00 PM
- End: 11:00 PM
- Repeat: every day
- Randomize times: no
- Selected lights:
  - Entryway — Entire Room
  - Family Room — Entire Room: floor lamp + Hue lightstrip
  - Listening Room — Entire Room

Light settings:

| Room | Scene / Mode |
|---|---|
| Entryway | Relax |
| Family Room | Dimmed |
| Listening Room | Sleepy |

---

## Lutron App — Schedules

App name shown: **Polk**. Current state shown: **All Off**.

| Source | Name | Trigger | Targets | Behavior | Decision | Notes |
|---|---|---|---|---|---|---|
| Lutron | Outdoor Lights | Sunset daily | Outdoor Lights | Turns outdoor lights on at sunset | Leave | Exterior lighting reliability matters; leave in Lutron for now. |
| Lutron | Outdoor Lights Off | 11:30 PM daily | Outdoor Lights | Turns outdoor lights off at 11:30 PM | Leave | Leave in Lutron for now. |
| Lutron | Smart Bridge 2 All Second Floor | Manual scene? | Broad second-floor scene | Existing HA scene `scene.smart_bridge_2_all_second_floor` | Review carefully | Broad scope; do not expose to agents casually. |

---

## Existing HA-Exposed Scenes / Items

| Source | Name | Trigger | Targets | Behavior | Decision | Notes |
|---|---|---|---|---|---|---|
| HA | Family Room Evening | Manual script | Kitchen, Family Room, Dining Room | Callable script `script.family_room_evening`; scene entity hidden from UI | Built / tested manually | Created 2026-06-01 via HA config API and reloaded. Corrected after first test: scene entity attributes must be flattened (`brightness`) rather than nested under `attributes`; script uses direct light service calls. Neima confirmed `script.turn_on` works from Developer Tools. The Family Room dashboard area scene trigger did not drive lights, so the working script was assigned to the `family_room` area and the scene entity was hidden from the UI to avoid the dead path. |
| HA | Family Room Movie | Manual script | Kitchen, Family Room, Dining Room | Callable script `script.family_room_movie`; scene entity hidden from UI | Built / tested manually | Created 2026-06-01 via HA config API and reloaded. Corrected after first test: scene entity attributes must be flattened (`brightness`) rather than nested under `attributes`; script uses direct light service calls. Neima confirmed `script.turn_on` works from Developer Tools. The Family Room dashboard area scene trigger did not drive lights, so the working script was assigned to the `family_room` area and the scene entity was hidden from the UI to avoid the dead path. |
| Hue | Family Room Dimmed | Manual scene | Family Room Hue lights | Existing scene `scene.family_room_dimmed`, brightness target 65 | Keep / ingredient | Does not include Lutron Family Room Main Lights. Use as ingredient only. |
| Hue | Entryway Relax | Manual scene | Entryway Hue lights | Existing scene `scene.entryway_relax`, brightness target 143 | Keep | Good dashboard candidate. |
| Hue | Entryway Bright 80% | Manual scene | Entryway Hue lights | Existing scene `scene.entryway_bright_80`, brightness target 205 | Keep | Good dashboard candidate. |
| Hue | Listening Room Read | Manual scene | Listening Room Hue lights | Existing scene `scene.listening_room_read`, brightness target 255 | Defer | Not first-pass daily dashboard unless Neima wants it. |
| Hue | Listening Room Relax | Manual scene | Listening Room Hue lights | Existing scene `scene.listening_room_relax`, brightness target 143 | Defer | Not first-pass daily dashboard unless Neima wants it. |
| Hue | Listening Room Warm Embrace | Manual scene | Listening Room Hue lights | Existing scene `scene.listening_room_warm_embrace`, brightness target 102 | Defer | Not first-pass daily dashboard unless Neima wants it. |
| Hue | Listening Room Sleepy | Manual scene | Listening Room Hue lights | Existing scene `scene.listening_room_sleepy`, brightness target 64 | Defer | Not first-pass daily dashboard unless Neima wants it. |
| Lutron | Smart Bridge 2 All Second Floor | Manual scene? | Broad second-floor scope | Existing scene `scene.smart_bridge_2_all_second_floor` | Review carefully | Broad scope; do not expose to agents casually. |

---

## First-Pass Migration Candidates

| Candidate | Priority | Proposed HA Owner | Decision | Notes |
|---|---:|---|---|---|
| Evening | 1 | HA script/scene | Build first | Exact translation of existing Apple Home scene across Kitchen, Family/Living, Dining. |
| Movie Mode | 1 | HA script/scene | Build second | Exact translation of existing Apple Home Movie scene. |
| Family Room Off | 2 | HA script | Build | Must include Hue group/lamp/lightstrip and Lutron main lights. |
| Kitchen / Dining Off | 2 | HA script | Build | Exact Lutron entity set. |
| Entryway Relax/Bright | 2 | Existing Hue scenes exposed in HA | Surface on dashboard | Can expose directly. |
| Common Lights Off | 3 | HA script | Build after target confirmation | Common areas only at first; decide whether to include Listening Room and bedrooms. |
| Google Home All Lights Off 11 PM | 4 | HA automation calling `script.common_lights_off` | Later | Only after the script is tested. |
| Hue Evening Lamps 5–11 PM | 5 | HA automation or leave in Hue | Later | Do not disable Hue version yet. |
| Hue Morning Lamp 7–9 AM | 6 | HA automation or leave in Hue | Later | Defer. |
| Lutron Outdoor schedules | 9 | Leave in Lutron | Leave | Exterior reliability; not worth moving now. |

---

## Proposed Exact HA Script Drafts

These are design drafts only. Do not apply without explicit approval.

### `scene.family_room_evening` / `script.family_room_evening`

- `light.kitchen_island_pendants`: on, brightness 30%
- `light.kitchen_main_lights`: off
- `light.tv_lightstrip`: on, brightness 28%
- `light.family_room_lamp`: on, brightness 75%
- `light.family_room_main_lights`: on, brightness 1%
- `light.dining_room_main_lights`: on, brightness 20%

Resolved: Neima confirmed Apple Home `Evening` should set the TV lightstrip to 28% brightness.

### `scene.family_room_movie` / `script.family_room_movie`

- `light.kitchen_island_pendants`: on, brightness 35%
- `light.tv_lightstrip`: on, brightness 19%
- `light.family_room_lamp`: on, brightness 25%
- `light.family_room_main_lights`: off
- `light.dining_room_main_lights`: off

### `script.common_lights_off`

Start conservative. Candidate targets:

- `light.kitchen_island_pendants`
- `light.kitchen_main_lights`
- `light.dining_room_main_lights`
- `light.family_room`
- `light.family_room_lamp`
- `light.tv_lightstrip`
- `light.family_room_main_lights`
- `light.entryway`
- `light.entry_lamp`

Open question: include `light.listening_room`? Do not include bedroom/exterior by default.

---

## Screenshots / Details Still Needed From Neima

Most core inventory is now usable. Remaining detail that would help:

1. Whether `All Lights Off` in Google Home literally includes bedroom, exterior, and listening room, or just common areas.
3. Whether Hue `Evening Lamps` should remain as a vendor-native ambience automation or be replaced after HA scenes are proven.
4. Whether Lutron outdoor schedules should remain permanently in Lutron — current recommendation: yes.

---

## Current Status

- [x] Inventory template created.
- [x] Existing HA-exposed scenes listed.
- [x] Apple Home Evening scene inventoried.
- [x] Apple Home Movie scene inventoried.
- [x] Google Home All Lights Off automation inventoried.
- [x] Hue app automations confirmed.
- [x] Lutron app schedules confirmed.
- [x] First HA replacement selected: Apple Home `Evening`, then `Movie`.
- [x] Neima approved exact HA `Evening` script spec, including TV lightstrip at 28%.
- [x] First HA scenes/scripts created and schema-corrected: `scene.family_room_evening`, `scene.family_room_movie`, `script.family_room_evening`, `script.family_room_movie`.
- [x] First HA scripts tested manually via Developer Tools `script.turn_on`; Neima confirmed it worked.
- [x] Family Room area control surface corrected: working script entities assigned to `family_room`; non-working scene trigger entities hidden from UI.
- [x] Dashboard buttons created in HA dashboard `Ned Home` at `/ned-home/home`; Family Room Modes buttons call `script.turn_on` for `script.family_room_evening` and `script.family_room_movie`.
