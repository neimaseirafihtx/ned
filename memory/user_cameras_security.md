---
name: cameras-security
description: Camera and security setup — Reolink + Nest Aware active, migration strategy to fully local
metadata:
  type: user
---

## Current Setup (Active)

- **Google Nest cameras** — current active cameras, paired with Nest Aware subscription
- **Nest Aware:** $100/yr — provides natural language video analysis ("black Tesla Model 3 parked", "man and dog walked by", "Amazon dropped off a package"). Coral TPU + Frigate cannot replicate this — it needs a vision LLM.

## Planned Hardware (On Hand / Ordered)

- **Reolink 810A cameras** — 4K, dual RTSP streams (`h264Preview_01_main` 4K, `h264Preview_01_sub` lower res), port 554. On hand.
- **Reolink NVR RLN8-410** — 8-channel PoE NVR. Planned. Handles ALL camera storage/recording (main stream, 24/7). Frigate pulls sub stream only.
- **Google Coral TPU** — USB accelerator for Frigate object detection on Mac Mini. Planned. Handles "person/car/dog detected" — not natural language descriptions.

## Migration Strategy

**Do NOT half-migrate.** Keep Nest Aware active until fully committed to replacing all cameras with Reolink. Running both systems creates unnecessary complexity.

**Full migration trigger:** Replace all Nest cameras with Reolink → ditch Nest Aware → then need a vision LLM to restore natural language descriptions.

**Vision LLM requirement:** Replacing Nest Aware's intelligent descriptions locally requires GPU compute (Windows RTX or Mac Mini upgrade to 48GB). This is the only use case that justifies GPU hardware.
