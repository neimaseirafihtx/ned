# Smart Home Scenes & Automations Inventory

---

## Apple Home — Scenes

### Scene: Evening

| Room | Accessory | State |
|------|-----------|-------|
| Kitchen | Island Pendants | 30% |
| Kitchen | Main Lights | Turn Off |
| Living Room | Hue Lightstrip | Turn On |
| Living Room | Lamp | 75% |
| Living Room | Main Lights | 1% |
| Dining Room | Main Lights | 20% |

---

### Scene: Movie

| Room | Accessory | State |
|------|-----------|-------|
| Kitchen | Island Pendants | 35% |
| Living Room | Hue Lightstrip | 19% |
| Living Room | Lamp | 25% |
| Living Room | Main Lights | Turn Off |
| Dining Room | Main Lights | Turn Off |

---

## Google Home — Automations

### Automation: All Lights Off
- **Trigger:** Scheduled — 11:00 PM daily
- **Next runs:** Today 11:00 PM, Tomorrow 11:00 PM

---

## Philips Hue — Automations

### Automation: Morning Lamp
- **Start:** 7:00 AM
- **End:** 9:00 AM
- **Repeat:** Every day (S M T W T F S — all selected)
- **Randomize Times:** No
- **Selected Lights:**
  - Entryway — Entire Room

---

### Automation: Evening Lamps
- **Start:** 5:00 PM
- **End:** 11:00 PM
- **Repeat:** Every day (S M T W T F S — all selected)
- **Randomize Times:** No
- **Selected Lights:**
  - Entryway — Entire Room
  - Family Room — Entire Room (floor lamp + Hue lightstrip)
  - Listening Room — Entire Room

#### Light Settings (Evening Lamps)
| Room | Scene/Mode |
|------|------------|
| Entryway | Relax |
| Family Room | Dimmed |
| Listening Room | Sleepy |

---

## Lutron (Polk) — Schedules

> App name shown: **Polk** | Current state shown: **All Off**

### Schedule: Outdoor Lights
- **Trigger:** At Sunset
- **Repeat:** Every day (S M T W T F S)
- **Status:** Enabled

### Schedule: Outdoor Lights Off
- **Trigger:** 11:30 PM
- **Repeat:** Every day (S M T W T F S)
- **Status:** Enabled

---

## Rooms / Zones Identified Across All Apps

| Room | Apps Where Referenced |
|------|-----------------------|
| Kitchen | Apple Home |
| Living Room | Apple Home, Google Home |
| Dining Room | Apple Home |
| Entryway | Philips Hue |
| Family Room | Philips Hue |
| Listening Room | Philips Hue |
| Outdoor | Lutron (Polk) |

---

## Devices / Accessories Identified

| Device | App | Room |
|--------|-----|------|
| Island Pendants | Apple Home | Kitchen |
| Main Lights | Apple Home | Kitchen, Living Room, Dining Room |
| Hue Lightstrip | Apple Home | Living Room |
| Lamp | Apple Home | Living Room |
| Entryway lights | Philips Hue | Entryway |
| Family Room lights | Philips Hue | Family Room |
| Listening Room lights | Philips Hue | Listening Room |
| Outdoor Lights | Lutron (Polk) | Outdoor |
