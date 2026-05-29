---
name: mac-mini-m4
description: Mac Mini M4 16GB — primary always-on home server, ordered and incoming as of 2026-05-25
metadata:
  type: user
---

Mac Mini M4 — primary home lab server. Always on.

- **Chip:** Apple M4 (base)
- **RAM:** 16GB unified memory
- **Status:** Ordered 2026-05-25, not yet arrived
- **Docker:** installed
- **External SSD:** 1-2TB planned (personal cloud storage only — not camera footage)

**Role:** Runs everything — Home Assistant VM (UTM), Ollama (8B for HA automation only), Frigate + Google Coral TPU, Nextcloud, Tailscale, Hermes Agent (migrating from MBP on arrival).

**Key constraint:** 16GB is tight for LLMs. Max 8B model for HA automation only — not a general inference machine. Heavy inference stays on MBP.

**Planned external SSD:** Samsung T9 1TB (USB 3.2) — for Nextcloud personal cloud only, not camera footage.

**Storage note:** NVR (RLN8-410) handles all camera recording. External SSD is personal cloud only.

**Google Coral TPU:** Planned for Frigate object detection offload. Handles "person/car/dog detected" fast and efficiently. Does NOT do natural language scene descriptions — that requires a vision LLM.
