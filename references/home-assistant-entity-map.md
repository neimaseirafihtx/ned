# Home Assistant Entity Map
*Generated 2026-05-29 from live HA API*

---

## Rooms & Key Entities

### Living Room
| Entity ID | Friendly Name | Type | Notes |
|-----------|--------------|------|-------|
| `media_player.living_room` | Living Room | Sonos Arc | TV audio playing (Dolby Atmos MAT 2.0), vol 12% |
| `media_player.75_the_frame` | 75" The Frame | Samsung TV | off |
| `sensor.living_room_audio_input_format` | Living Room Audio input format | sensor | "Dolby Atmos (MAT 2.0)" |

### Family Room
| Entity ID | Friendly Name | Type | Notes |
|-----------|--------------|------|-------|
| `light.family_room` | Family Room | Hue group | ON — TV lightstrip + lamp (blue/purple, 30% brightness) |
| `light.family_room_lamp` | Family Room Lamp | Hue bulb | off |
| `light.tv_lightstrip` | TV lightstrip | Hue lightstrip | ON — blue/purple |
| `light.family_room_main_lights` | Family Room Main Lights | Lutron Caseta | off |
| `scene.family_room_dimmed` | Family Room Dimmed | Hue scene | — |

### Kitchen
| Entity ID | Friendly Name | Type | Notes |
|-----------|--------------|------|-------|
| `light.kitchen_main_lights` | Kitchen Main Lights | Lutron Caseta | off |
| `light.kitchen_island_pendants` | Kitchen Island Pendants | Lutron Caseta | off |

### Dining Room
| Entity ID | Friendly Name | Type | Notes |
|-----------|--------------|------|-------|
| `light.dining_room_main_lights` | Dining Room Main Lights | Lutron Caseta | off |

### Entryway
| Entity ID | Friendly Name | Type | Notes |
|-----------|--------------|------|-------|
| `light.entryway` | Entryway | Hue group | off (Entry Lamp) |
| `light.entry_lamp` | Entry Lamp | Hue bulb | off |
| `scene.entryway_bright_80` | Entryway Bright 80% | Hue scene | — |
| `scene.entryway_relax` | Entryway Relax | Hue scene | — |

### Listening Room
| Entity ID | Friendly Name | Type | Notes |
|-----------|--------------|------|-------|
| `media_player.listening_room` | Listening Room | Sonos (surround setup) | paused — Chris Stapleton |
| `light.listening_room` | Listening Room | Hue group | off |
| `light.listening_room_lamp` | Listening Room Lamp | Hue bulb | **UNAVAILABLE** — check if offline |
| `scene.listening_room_read` | Listening Room Read | Hue scene | — |
| `scene.listening_room_relax` | Listening Room Relax | Hue scene | — |
| `scene.listening_room_warm_embrace` | Listening Room Warm Embrace | Hue scene | — |
| `scene.listening_room_sleepy` | Listening Room Sleepy | Hue scene | — |

### Master Bedroom
| Entity ID | Friendly Name | Type | Notes |
|-----------|--------------|------|-------|
| `light.master_bedroom_main_lights` | Master Bedroom Main Lights | Lutron Caseta | off |
| `media_player.neimas_room` | Neima's Room | Sonos | idle |

### Office
| Entity ID | Friendly Name | Type | Notes |
|-----------|--------------|------|-------|
| `media_player.office` | Office | Sonos | paused — Sabrina Carpenter |
| `binary_sensor.office_microphone` | Office Microphone | sensor | **on** (mic active) |

### Garage
| Entity ID | Friendly Name | Type | Notes |
|-----------|--------------|------|-------|
| `media_player.garage` | Garage | Sonos | paused — GELO |

### Guestroom
| Entity ID | Friendly Name | Type | Notes |
|-----------|--------------|------|-------|
| `light.guestroom_main_lights` | Guestroom Main Lights | Lutron Caseta | off |

### Exterior
| Entity ID | Friendly Name | Type | Notes |
|-----------|--------------|------|-------|
| `light.exterior_driveway_light` | Exterior Driveway Light | Lutron Caseta | off |

---

## Displays / TVs
| Entity ID | Friendly Name | State |
|-----------|--------------|-------|
| `media_player.75_the_frame` | 75" The Frame | off |
| `media_player.65_oled` | 65" OLED | **unavailable** |
| `media_player.bedroom_display` | Bedroom Display | off |

---

## Network & System
| Entity ID | Friendly Name | State |
|-----------|--------------|-------|
| `binary_sensor.be63_wan_status` | BE63 WAN status | on (connected) |
| `sensor.be63_external_ip` | BE63 External IP | 70.228.12.186 |
| `sensor.be63_download_speed` | BE63 Download speed | ~1385 KiB/s |
| `sensor.be63_upload_speed` | BE63 Upload speed | ~155 KiB/s |
| `weather.forecast_home` | Forecast Home | sunny, 89°F, 60% humidity |
| `person.neima_seirafi` | Neima Seirafi | unknown (no device trackers) |

---

## Hue Automations
| Entity ID | Friendly Name | State |
|-----------|--------------|-------|
| `switch.hue_bridge_automation_evening_lamps` | Evening Lamps automation | **on** |
| `switch.hue_bridge_automation_morning_lamp` | Morning Lamp automation | **on** |

---

## Notes & Cleanup Items

**Duplicate/confusing entities to be aware of:**
- `media_player.*_2` entities — Music Assistant virtual players for the same Sonos speakers. Use the non-`_2` entities for agent control unless specifically using Music Assistant.
- `media_player.neima_s_bedroom` — unavailable, appears to be a stale/ghost Music Assistant player separate from `media_player.neimas_room`. Can likely be deleted.
- `media_player.living_room_2_2` — unavailable "Living Room (2)" Music Assistant player. Same issue.

**Things to fix:**
- `light.listening_room_lamp` — UNAVAILABLE. Bulb may be off at the switch or unplugged.
- `media_player.65_oled` — unavailable. TV may be powered off with no network standby, or integration needs attention.
- `person.neima_seirafi` — no device trackers configured. Add phone to enable presence detection.

**Intentionally omitted (too noisy for agents):**
- Sonos EQ controls (bass, treble, balance, surround level, sub gain, etc.)
- Sonos behavior switches (crossfade, loudness, night sound, speech enhancement, TV autoplay, etc.)
- Backup/system sensors
- Sun position sensors
- HA update entities
- Music Assistant `_2` player duplicates
