# Home Assistant Entity Map
*Generated 2026-05-29 from live HA API; cross-checked 2026-05-29 18:58 CDT via Home Assistant MCP `GetLiveContext`*

---

## Purpose

This is a curated agent-facing map of useful Home Assistant entities. It is intentionally not a raw entity dump.

Use this file for stable names, safe-control targets, and cleanup notes. For current state, prefer live Home Assistant MCP reads with `GetLiveContext`.

---

## Current MCP Cross-Check Notes

Read-only MCP comparison ran against the official Home Assistant MCP Server with `GetLiveContext` only. No write/control/media/broadcast/todo mutation tools were called.

Important differences from the original HA API snapshot:

- Several light state notes are naturally time-sensitive and changed live:
  - After the first approved write test, Family Room lights were around 30% raw brightness (`light.family_room_main_lights` verified at raw brightness 76).
  - Entryway / Entry Lamp are currently on at brightness 143.
  - Listening Room light is currently on at brightness 65.
- Media players often appear more than once in MCP live context because HA exposes both display/player and speaker/duplicate contexts. Treat entity IDs below as canonical where known, and use friendly names carefully when reading MCP output.
- `light.listening_room_lamp` remains unavailable.
- `media_player.65_oled` still has an unavailable display context, but MCP also exposes an idle speaker-like duplicate.
- Network/system sensors and Hue automation switches from the HA API snapshot were not present in the current MCP exposed live context; keep them as useful API-snapshot references, not as validated MCP-exposed entities.

---

## Rooms & Key Entities

### Living Room / Family Room Media
| Entity ID | Friendly Name | Type | Notes |
|-----------|--------------|------|-------|
| `media_player.living_room` | Living Room | Sonos Arc | MCP live: playing TV / TV Audio, vol ~6%. Use non-`_2` entity for normal Sonos status/control. |
| `media_player.75_the_frame` | 75" The Frame | Samsung TV | MCP live exposes multiple contexts: TV in Family Room is on, vol ~12%; duplicate/off/idle speaker contexts also appear. |
| `sensor.living_room_audio_input_format` | Living Room Audio input format | sensor | HA API snapshot previously showed "Dolby Atmos (MAT 2.0)"; not exposed in current MCP live context. |

### Family Room Lights
| Entity ID | Friendly Name | Type | Notes |
|-----------|--------------|------|-------|
| `light.family_room` | Family Room | Hue group | Current after Telegram follow-up fix: off. Group includes TV lightstrip + lamp, but not the Lutron main lights. |
| `light.family_room_lamp` | Family Room Lamp | Hue bulb | Current after Telegram follow-up fix: off. |
| `light.tv_lightstrip` | TV lightstrip | Hue lightstrip | Current after Telegram follow-up fix: off. Good low-risk visible write-test target if explicitly approved. |
| `light.family_room_main_lights` | Family Room Main Lights | Lutron Caseta | Current after Telegram follow-up fix: off. Important: include this when user says “Family Room lights”; Hue group turn-off alone misses it. |
| `scene.family_room_dimmed` | Family Room Dimmed | Hue scene | MCP live: scene exposed, unknown state, brightness target 65. |

Family Room control note:
- Treat “Family Room lights” as all four light entities above: `light.family_room`, `light.family_room_lamp`, `light.tv_lightstrip`, and `light.family_room_main_lights`.
- The 2026-05-29 Telegram “turn off Family Room lights” attempt initially missed `light.family_room_main_lights` because it targeted the Hue group/child lights but not the separate Lutron main lights. Exact REST turn-off of `light.family_room_main_lights` fixed the remaining light.
- For future exact family-room-off routines, prefer an allowlisted exact entity set or a Home Assistant group intentionally containing both Hue and Lutron entities.

### Kitchen
| Entity ID | Friendly Name | Type | Notes |
|-----------|--------------|------|-------|
| `light.kitchen_main_lights` | Kitchen Main Lights | Lutron Caseta | MCP live: off. |
| `light.kitchen_island_pendants` | Kitchen Island Pendants | Lutron Caseta | MCP live: off. |

### Dining Room
| Entity ID | Friendly Name | Type | Notes |
|-----------|--------------|------|-------|
| `light.dining_room_main_lights` | Dining Room Main Lights | Lutron Caseta | MCP live: off. |

### Entryway
| Entity ID | Friendly Name | Type | Notes |
|-----------|--------------|------|-------|
| `light.entryway` | Entryway | Hue group | MCP live: on, brightness 143. |
| `light.entry_lamp` | Entry Lamp | Hue bulb | MCP live: on, brightness 143. |
| `scene.entryway_bright_80` | Entryway Bright 80% | Hue scene | MCP live: scene exposed, unknown state, brightness target 205. |
| `scene.entryway_relax` | Entryway Relax | Hue scene | MCP live: scene exposed, unknown state, brightness target 143. Good low-risk visible scene test if explicitly approved. |

### Listening Room
| Entity ID | Friendly Name | Type | Notes |
|-----------|--------------|------|-------|
| `media_player.listening_room` | Listening Room | Sonos (surround setup) | MCP live: paused, Chris Stapleton — "You Should Probably Leave", vol ~47%. Duplicate non-area context also appears. |
| `light.listening_room` | Listening Room | Hue group | MCP live: on, brightness 65. |
| `light.listening_room_lamp` | Listening Room Lamp | Hue bulb | MCP live: **unavailable** — still a cleanup item. |
| `scene.listening_room_read` | Listening Room Read | Hue scene | MCP live: scene exposed, unknown state, brightness target 255. |
| `scene.listening_room_relax` | Listening Room Relax | Hue scene | MCP live: scene exposed, unknown state, brightness target 143. |
| `scene.listening_room_warm_embrace` | Listening Room Warm Embrace | Hue scene | MCP live: scene exposed, unknown state, brightness target 102. |
| `scene.listening_room_sleepy` | Listening Room Sleepy | Hue scene | MCP live: scene exposed, unknown state, brightness target 64. |

### Master Bedroom / Neima’s Room
| Entity ID | Friendly Name | Type | Notes |
|-----------|--------------|------|-------|
| `light.master_bedroom_main_lights` | Master Bedroom Main Lights | Lutron Caseta | MCP live: off; area appears as Neima’s Room. |
| `media_player.neimas_room` | Neima's Room | Sonos | MCP live friendly name appears as Neima’s Room: idle in area context, plus paused duplicate with media title "Spotify", vol ~51%. |

### Office
| Entity ID | Friendly Name | Type | Notes |
|-----------|--------------|------|-------|
| `media_player.office` | Office | Sonos | MCP live: paused, Sabrina Carpenter — "Manchild", vol ~20%. Duplicate non-area context also appears. |
| `binary_sensor.office_microphone` | Office Microphone | sensor | HA API snapshot previously showed on / mic active; not exposed in current MCP live context. |

### Garage
| Entity ID | Friendly Name | Type | Notes |
|-----------|--------------|------|-------|
| `media_player.garage` | Garage | Sonos | MCP live: paused, GELO — "Tweaker", vol ~27%. Duplicate non-area context also appears. |

### Guestroom
| Entity ID | Friendly Name | Type | Notes |
|-----------|--------------|------|-------|
| `light.guestroom_main_lights` | Guestroom Main Lights | Lutron Caseta | MCP live: off. |

### Exterior
| Entity ID | Friendly Name | Type | Notes |
|-----------|--------------|------|-------|
| `light.exterior_driveway_light` | Exterior Driveway Light | Lutron Caseta | MCP live: off. |

---

## Displays / TVs
| Entity ID | Friendly Name | State / MCP Note |
|-----------|--------------|------------------|
| `media_player.75_the_frame` | 75" The Frame | MCP live has multiple contexts: TV is on in Family Room, plus off/idle duplicate contexts. |
| `media_player.65_oled` | 65" OLED | MCP live: unavailable in Neima’s Room display context; idle speaker-like duplicate also exposed. |
| `media_player.bedroom_display` | Bedroom Display | MCP live: off in Neima’s Room display context; idle speaker-like duplicate also exposed. |

---

## Network & System
| Entity ID | Friendly Name | State / Notes |
|-----------|--------------|---------------|
| `binary_sensor.be63_wan_status` | BE63 WAN status | HA API snapshot: on / connected; not present in current MCP live context. |
| `sensor.be63_external_ip` | BE63 External IP | HA API snapshot included an external IP; do not copy current values into chat unless needed. Not present in current MCP live context. |
| `sensor.be63_download_speed` | BE63 Download speed | HA API snapshot: present; not present in current MCP live context. |
| `sensor.be63_upload_speed` | BE63 Upload speed | HA API snapshot: present; not present in current MCP live context. |
| `weather.forecast_home` | Forecast Home | HA API snapshot: present; not present in current MCP live context. |
| `person.neima_seirafi` | Neima Seirafi | HA API snapshot: unknown / no device trackers; not present in current MCP live context. |

---

## Hue Automations
| Entity ID | Friendly Name | State / Notes |
|-----------|--------------|---------------|
| `switch.hue_bridge_automation_evening_lamps` | Evening Lamps automation | HA API snapshot: on; not present in current MCP live context. |
| `switch.hue_bridge_automation_morning_lamp` | Morning Lamp automation | HA API snapshot: on; not present in current MCP live context. |

---

## Additional MCP-Exposed Entities Worth Knowing

These appeared in `GetLiveContext` and may be useful for status questions, but are not primary control targets right now:

| Friendly Name | Domain | MCP Live Note |
|---------------|--------|---------------|
| Neima’s Mac mini | `media_player` | idle, vol ~20%; likely always-on server/audio endpoint. |
| Neima’s MacBook Pro | `media_player` | idle, vol ~20%; workstation audio endpoint. |
| Shopping List | `todo` | state 0; read-only queries are safe, mutations still require approval. |
| Smart Bridge 2 Unassigned Smart Away | `switch` | off; treat as automation/security-ish and do not toggle without explicit approval. |
| Smart Bridge 2 All Second Floor | `scene` | unknown; not a first-choice test scene. |

---

## Notes & Cleanup Items

**Duplicate/confusing entities to be aware of:**
- `media_player.*_2` entities — Music Assistant virtual players for the same Sonos speakers. Use the non-`_2` entities for agent control unless specifically using Music Assistant.
- `media_player.neima_s_bedroom` — unavailable, appears to be a stale/ghost Music Assistant player separate from `media_player.neimas_room`. Can likely be deleted.
- `media_player.living_room_2_2` / friendly name "Living Room (2)" — unavailable Music Assistant player. Same issue.
- MCP `GetLiveContext` can show multiple records with the same friendly name for display/player/speaker contexts. Prefer entity IDs from this map when planning control actions.

**Things to fix or intentionally accept:**
- `light.listening_room_lamp` — still unavailable in MCP live context; Neima previously noted this is intentional because it is off at the switch.
- `media_player.65_oled` — still has an unavailable display context; Neima previously noted this is expected for a rarely used TV.
- `person.neima_seirafi` — no device trackers configured in the HA API snapshot. Add phone tracking if presence detection becomes useful.
- Decide whether network/system sensors should be exposed through MCP, or keep them API-only/static-reference for now.

**Intentionally omitted or de-prioritized for agents:**
- Sonos EQ controls (bass, treble, balance, surround level, sub gain, etc.)
- Sonos behavior switches (crossfade, loudness, night sound, speech enhancement, TV autoplay, etc.)
- Backup/system sensors
- Sun position sensors
- HA update entities
- Music Assistant `_2` player duplicates
