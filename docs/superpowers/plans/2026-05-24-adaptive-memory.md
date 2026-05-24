# Adaptive Memory Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add session-logging + `/note`-triggered deep memory review to the Ned agent, giving it Hermes-style continuous observation and consolidation without a background daemon.

**Architecture:** Three parts — (1) a real-time session log that Ned appends to silently during conversation, (2) a `/note` slash command that deep-reviews the full conversation + log and writes typed memory files, (3) additions to `CLAUDE.md` that wire up the always-on watching behavior and session-start memory load. All behavior is instruction-driven (markdown files); no code, no daemon.

**Tech Stack:** Claude Code slash commands (`.claude/commands/*.md`), markdown memory files, CLAUDE.md project instructions.

---

### Task 1: Create memory directory and stub files

**Files:**
- Create: `memory/MEMORY.md`
- Create: `memory/session-log.md`

- [ ] **Step 1: Create `memory/MEMORY.md`**

Create the file at `memory/MEMORY.md` with this exact content:

```markdown
# Ned Memory Index

<!-- One line per memory file: - [Title](filename.md) — one-line hook -->
```

- [ ] **Step 2: Create `memory/session-log.md`**

Create the file at `memory/session-log.md` with this exact content:

```markdown
<!-- Session observation log. Format: [YYYY-MM-DD] [type] observation -->
<!-- Cleared automatically when /note is run. -->
```

- [ ] **Step 3: Verify files exist**

Run:
```bash
ls memory/
```
Expected output:
```
MEMORY.md       session-log.md
```

- [ ] **Step 4: Commit**

```bash
git add memory/MEMORY.md memory/session-log.md
git commit -m "feat: add memory directory with stub files"
```

---

### Task 2: Create `.claude/commands/note.md` (the `/note` slash command)

**Files:**
- Create: `.claude/commands/note.md`

- [ ] **Step 1: Create the commands directory**

```bash
mkdir -p .claude/commands
```

- [ ] **Step 2: Create `.claude/commands/note.md`**

Create the file with this exact content:

```markdown
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
```

- [ ] **Step 3: Verify the command file is in place**

```bash
ls .claude/commands/
```
Expected:
```
note.md
```

- [ ] **Step 4: Commit**

```bash
git add .claude/commands/note.md
git commit -m "feat: add /note adaptive memory slash command"
```

---

### Task 3: Update `CLAUDE.md` with watching and memory-load instructions

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Add the Adaptive Memory section to `CLAUDE.md`**

Append the following section to the end of `CLAUDE.md` (after the "Adding new context" section):

```markdown
## Adaptive Memory

At the start of each session, read `memory/MEMORY.md`. Load the memory files listed there that are relevant to the current question — same pattern as loading from `references/`.

During every conversation, watch for these signals and append a tagged one-liner to `memory/session-log.md` when spotted. Do this silently — use the Write/Edit tool with no text commentary around it:

| Signal | Tag | Example entry |
|--------|-----|---------------|
| Explicit correction ("no", "stop X", "actually...") | `[feedback]` | `[2026-05-24] [feedback] user prefers raw commands over step-by-step` |
| Confirmed preference (unusual approach accepted without pushback) | `[feedback]` | `[2026-05-24] [feedback] single bundled PR preferred over split PRs` |
| New hardware/config fact | `[user]` | `[2026-05-24] [user] RTX 3090 confirmed as Windows desktop GPU` |
| New project context (goal, decision, phase status, timeline) | `[project]` | `[2026-05-24] [project] Tailscale setup complete` |
| External resource identified | `[reference]` | `[2026-05-24] [reference] Grafana board at X is oncall dashboard` |

Append to `memory/session-log.md`, do not overwrite it. The `/note` command handles consolidation and cleanup.
```

- [ ] **Step 2: Verify the addition looks correct**

```bash
tail -30 CLAUDE.md
```

Confirm the Adaptive Memory section appears with the correct table and no truncation.

- [ ] **Step 3: Commit**

```bash
git add CLAUDE.md
git commit -m "feat: add adaptive memory watching and session-start load to CLAUDE.md"
```

---

### Task 4: Smoke test

No code to test — verify the full flow works end-to-end manually.

- [ ] **Step 1: Verify `/note` command is discoverable**

In a Claude Code session in this project, type `/note`. Confirm the command appears in autocomplete and runs the deep review prompt from `.claude/commands/note.md`.

- [ ] **Step 2: Verify session-log writes**

Say something in the session that should trigger a log entry (e.g., "the Windows GPU is an RTX 3080"). Confirm Ned appends a `[user]` entry to `memory/session-log.md` without announcing it.

- [ ] **Step 3: Verify `/note` consolidation**

Run `/note`. Confirm:
- A new memory file appears in `memory/` for the RTX 3080 fact
- `memory/MEMORY.md` has an entry for it
- `memory/session-log.md` is cleared back to comment lines
- A summary is printed

- [ ] **Step 4: Verify memory load at session start**

Start a fresh session. Confirm Ned reads `memory/MEMORY.md` before answering the first question and loads the RTX 3080 file.
