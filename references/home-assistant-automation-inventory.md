# Home Assistant Automation / Scene Inventory

**Created:** 2026-06-01  
**Purpose:** Inventory existing Google Home, Hue, and Lutron routines before recreating anything in Home Assistant.

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

## Known Items From HA Snapshot

| Source | Name | Trigger | Targets | Behavior | Decision | Notes |
|---|---|---|---|---|---|---|
| Hue | Evening Lamps automation | Unknown | Unknown lamps | Existing Hue Bridge automation exposed in HA API snapshot as `switch.hue_bridge_automation_evening_lamps` | Inventory | Need screenshot/details from Hue app before migration. |
| Hue | Morning Lamp automation | Unknown | Unknown lamp(s) | Existing Hue Bridge automation exposed in HA API snapshot as `switch.hue_bridge_automation_morning_lamp` | Inventory | Need screenshot/details from Hue app before migration. |
| Hue | Family Room Dimmed | Manual scene | Family Room Hue lights | Existing scene `scene.family_room_dimmed`, brightness target 65 | Keep / ingredient | Does not include Lutron Family Room Main Lights. Use as ingredient only. |
| Hue | Entryway Relax | Manual scene | Entryway Hue lights | Existing scene `scene.entryway_relax`, brightness target 143 | Keep | Good dashboard candidate. |
| Hue | Entryway Bright 80% | Manual scene | Entryway Hue lights | Existing scene `scene.entryway_bright_80`, brightness target 205 | Keep | Good dashboard candidate. |
| Hue | Listening Room Read | Manual scene | Listening Room Hue lights | Existing scene `scene.listening_room_read`, brightness target 255 | Defer | Not first-pass daily dashboard unless Neima wants it. |
| Hue | Listening Room Relax | Manual scene | Listening Room Hue lights | Existing scene `scene.listening_room_relax`, brightness target 143 | Defer | Not first-pass daily dashboard unless Neima wants it. |
| Hue | Listening Room Warm Embrace | Manual scene | Listening Room Hue lights | Existing scene `scene.listening_room_warm_embrace`, brightness target 102 | Defer | Not first-pass daily dashboard unless Neima wants it. |
| Hue | Listening Room Sleepy | Manual scene | Listening Room Hue lights | Existing scene `scene.listening_room_sleepy`, brightness target 64 | Defer | Not first-pass daily dashboard unless Neima wants it. |
| Lutron | Smart Bridge 2 All Second Floor | Manual scene? | Broad second-floor scope | Existing scene `scene.smart_bridge_2_all_second_floor` | Review carefully | Broad scope; do not expose to agents casually. |

---

## Google Home Inventory

Fill this from Google Home app screenshots or manual review.

| Source | Name | Trigger | Targets | Behavior | Decision | Notes |
|---|---|---|---|---|---|---|
| Google Home |  | Voice/manual/time/presence |  |  |  |  |
| Google Home |  | Voice/manual/time/presence |  |  |  |  |
| Google Home |  | Voice/manual/time/presence |  |  |  |  |
| Google Home |  | Voice/manual/time/presence |  |  |  |  |

Checklist while reviewing Google Home:

- Routines / Automations tab.
- Household routines and personal routines.
- Voice phrases that actually matter.
- Time-based routines.
- Presence-based routines.
- Any routines that control lights, TVs, Sonos, thermostats, security, or cameras.

---

## Hue App Inventory

| Source | Name | Trigger | Targets | Behavior | Decision | Notes |
|---|---|---|---|---|---|---|
| Hue | Evening Lamps automation | Unknown | Unknown |  | Inventory | Confirm trigger/targets in Hue app. |
| Hue | Morning Lamp automation | Unknown | Unknown |  | Inventory | Confirm trigger/targets in Hue app. |
| Hue |  |  |  |  |  |  |
| Hue |  |  |  |  |  |  |

Checklist while reviewing Hue:

- Automations.
- Scenes per room.
- Time/sunset/sunrise behavior.
- Motion sensors, if any.
- Which Hue scenes are actually used vs default clutter.

---

## Lutron App Inventory

| Source | Name | Trigger | Targets | Behavior | Decision | Notes |
|---|---|---|---|---|---|---|
| Lutron | Smart Bridge 2 All Second Floor | Manual? | Broad second-floor scene |  | Review | Exists in HA as `scene.smart_bridge_2_all_second_floor`. |
| Lutron |  |  |  |  |  |  |
| Lutron |  |  |  |  |  |  |
| Lutron |  |  |  |  |  |  |

Checklist while reviewing Lutron:

- Scenes.
- Schedules.
- Pico remotes and button actions.
- Smart Away / security-like features.
- Any exterior lighting schedules.
- Anything that should remain Lutron-native for reliability.

---

## First-Pass Migration Candidates

| Candidate | Priority | Proposed HA Owner | Notes |
|---|---:|---|---|
| Family Room Off | 1 | HA script | Must include Hue group/lamp/lightstrip and Lutron main lights. |
| Family Room Relax | 1 | HA script/scene | First daily-use dashboard button. |
| Movie Mode | 2 | HA script/scene | Need Neima preference: main lights fully off vs low. |
| Kitchen / Dining Off | 2 | HA script | Exact Lutron entity set. |
| Entryway Relax/Bright | 2 | Existing Hue scenes exposed in HA | Can surface directly on dashboard. |
| Common Lights Off | 3 | HA script | Common areas only; no bedrooms/exterior/security. |
| Night / Shutdown | 3 | HA script + later automation | Define carefully after app inventory. |
| Morning | 4 | HA automation/script | Do after inventorying Hue Morning Lamp + Google routines. |

---

## Screenshots Needed From Neima

To finish inventory without guessing, collect screenshots or names from:

1. Google Home → Automations / Routines.
2. Hue → Automations.
3. Hue → Room scenes for Family Room, Entryway, Listening Room.
4. Lutron → Scenes.
5. Lutron → Schedules.
6. HA Companion App dashboard if already installed.

Minimum viable screenshot set:

- Google Home Automations list.
- Hue Automations list.
- Lutron Scenes/Schedules list.

---

## Current Status

- [x] Inventory template created.
- [x] Existing HA-exposed scenes listed.
- [x] Known Hue Bridge automations from HA snapshot listed.
- [ ] Google Home routines inventoried.
- [ ] Hue app automations confirmed.
- [ ] Lutron app scenes/schedules confirmed.
- [ ] First HA replacement selected.
