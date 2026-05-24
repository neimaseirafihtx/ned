# Adaptive Memory — Design Spec

**Date:** 2026-05-24
**Trigger:** `/note`
**Scope:** ned project only (`Documents/Claude/ned/`)

---

## Overview

Adaptive Memory gives Ned two continuous behaviors:

1. **Real-time watching** — passively observes the conversation each session and logs noteworthy moments to a staging file on disk as they happen
2. **Deep review at `/note`** — when triggered, processes the session log + full conversation + existing memories, writes consolidated updates to typed memory files, clears the log, reports what changed

Inspired by Hermes Agent's auto-retain (per-turn extraction) and curator (background consolidation) patterns, adapted for a skill-based Claude Code agent with no background daemon.

---

## File Structure

```
Documents/Claude/ned/
  CLAUDE.md                       ← add watching + memory-load instructions
  .claude/commands/note.md        ← /note slash command definition
  memory/
    MEMORY.md                     ← index of all memory files (one line per file)
    session-log.md                ← real-time observation staging area (cleared at /note)
    user_<slug>.md                ← user profile facts
    feedback_<slug>.md            ← corrections and confirmed preferences
    project_<slug>.md             ← project context, decisions, timelines
    reference_<slug>.md           ← pointers to external resources
```

Memory files use the same typed frontmatter as the system memory:

```markdown
---
name: slug
description: one-line summary
metadata:
  type: user | feedback | project | reference
---
content here
```

---

## Component 1: Real-Time Watching (CLAUDE.md addition)

Ned watches every conversation turn for these signals:

| Signal | Memory type | Example |
|--------|-------------|---------|
| Explicit correction ("no, don't", "stop X", "actually...") | feedback | user prefers raw commands over step-by-step |
| Preference confirmed (accepts unusual approach without pushback) | feedback | single bundled PR preferred for refactors |
| New hardware/config fact | user | RTX 3090 confirmed as Windows desktop GPU |
| New project context | project | Frigate setup starting after cameras arrive |
| External resource identified | reference | Grafana board at X is the oncall dashboard |

When a signal is spotted, Ned appends a tagged one-liner to `memory/session-log.md`:

```
[2026-05-24] [feedback] user prefers direct commands over step-by-step explanation
[2026-05-24] [user] RTX 3090 confirmed as Windows desktop GPU
[2026-05-24] [project] Frigate setup begins after Reolink cameras arrive
```

Ned does **not** interrupt the conversation to announce log writes.

**Session start:** Ned reads `memory/MEMORY.md` and loads relevant memory files before answering, the same way it loads from `references/`.

---

## Component 2: `/note` Deep Review

Triggered by `/note`. Steps:

1. Read `memory/session-log.md`
2. Read all existing memory files
3. Scan the full conversation for anything the session log missed
4. For each observation: create a new typed file, update an existing one, or delete a stale one
5. Update `memory/MEMORY.md` index
6. Clear `memory/session-log.md`
7. Print a short summary:

```
Adaptive memory updated:
  + added: feedback_response_style.md
  ~ updated: project_homelab.md (RTX 3090 added)
  - removed: project_remote_access.md (Tailscale confirmed complete)
```

Writes directly — no approval step.

---

## Implementation Files

| File | Action |
|------|--------|
| `CLAUDE.md` | Add: watching instructions + session-start memory load |
| `.claude/commands/note.md` | Create: `/note` slash command |
| `memory/MEMORY.md` | Create: empty index |
| `memory/session-log.md` | Create: empty staging file |

---

## Out of Scope

- No background daemon or cron — all behavior is instruction-driven
- No vector search or embeddings — plain markdown files
- No approval gate before writes
- Deduplication between session-log entries and full conversation scan handled by the `/note` review step (not a separate pass)
