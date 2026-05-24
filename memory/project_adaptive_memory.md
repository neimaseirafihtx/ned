---
name: adaptive-memory
description: Adaptive Memory system built for Ned — /note command, session log, typed memory files
metadata:
  type: project
---

Adaptive Memory system is live as of 2026-05-24.

**How it works:**
- During sessions, Ned silently appends tagged observations to `memory/session-log.md`
- `/note` command triggers a full conversation review: reads log + existing memory, writes/updates/deletes typed memory files, updates `memory/MEMORY.md` index, clears the log, prints summary

**Memory file types:** `feedback_*.md` (always load), `user_*.md`, `project_*.md`, `reference_*.md`

**Spec and plan:** `docs/superpowers/specs/2026-05-24-adaptive-memory-design.md` and `docs/superpowers/plans/2026-05-24-adaptive-memory.md`

**Why:** Persistent learning across sessions without a background daemon — instruction-driven, markdown-only, all files in the ned project folder.
