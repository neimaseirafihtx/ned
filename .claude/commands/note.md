Run adaptive memory deep review. Follow these steps exactly:

## Step 1: Read existing state

Read `memory/session-log.md`. If it exists and has content beyond the comment lines, note all entries. If empty or missing, skip to Step 2.

Read `memory/MEMORY.md` to get the index of existing memory files, then read each file listed there.

## Step 2: Full conversation scan

Scan the entire conversation from the beginning. Extract every signal worth capturing:

| Signal type | Memory type | Examples |
|-------------|-------------|---------|
| Explicit correction ("no", "stop X", "actually...") | feedback | response style, approach preferences |
| Confirmed preference (accepted unusual approach without pushback) | feedback | bundled PRs, terse answers |
| Hardware/config fact | user | GPU model, network setup, software versions |
| Project context (new goal, decision, timeline, phase status) | project | phase complete, new hardware arriving |
| External resource identified | reference | dashboards, docs, issue trackers |

Combine with the session-log entries. Deduplicate.

## Step 3: Write memory updates

For each observation:

**New memory:** Create a typed file at `memory/<type>_<slug>.md` using this frontmatter:

```
---
name: slug-here
description: one-line summary used to decide relevance in future sessions
metadata:
  type: user | feedback | project | reference
---

Content here. For feedback/project: lead with the rule/fact, then **Why:** and **How to apply:** lines.
```

**Update existing memory:** Edit the relevant file in place — replace stale facts, add new details, remove contradictions.

**Remove stale memory:** Delete files for facts that are no longer true (e.g., a phase marked complete, a hardware guess that's now confirmed differently).

**Update index:** After all writes, update `memory/MEMORY.md` so every current memory file has exactly one entry:
```
- [Title](filename.md) — one-line hook (under 150 chars)
```

## Step 4: Clear the session log

Overwrite `memory/session-log.md` with just the comment lines:

```
<!-- Session observation log. Format: [YYYY-MM-DD] [type] observation -->
<!-- Cleared automatically when /note is run. -->
```

## Step 5: Print summary

Output a short report of what changed:

```
Adaptive memory updated:
  + added: <filename> — <one-line description>
  ~ updated: <filename> — <what changed>
  - removed: <filename> — <why>
```

If nothing changed, say: "No new learnings to capture from this session."
