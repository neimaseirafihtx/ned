# Hermes Agent — Comprehensive Reference

> A reference document for another Claude instance. All facts here come from `hermes-agent.nousresearch.com/docs`, the GitHub repo `NousResearch/hermes-agent`, and linked primary sources. Current as of Hermes Agent **v0.14.0** (release tag `v2026.5.16`, May 16, 2026).

---

## 1. What is Hermes Agent?

Hermes Agent is an **open-source, MIT-licensed, self-improving autonomous AI agent** built by **Nous Research**. Tagline: *"The agent that grows with you."* Unlike coding copilots tied to an IDE or chatbot wrappers around a single API, Hermes is designed to live on a server (a $5 VPS, GPU cluster, or serverless infrastructure like Daytona/Modal that costs near-zero when idle) and accept instructions from wherever the user is — CLI, Telegram, Discord, Slack, WhatsApp, Signal, Email, SMS, etc.

Official self-description: *"The self-improving AI agent built by Nous Research. The only agent with a built-in learning loop — it creates skills from experience, improves them during use, nudges itself to persist knowledge, and builds a deepening model of who you are across sessions."*

### Design philosophy — the "closed learning loop"

- **Agent-curated persistent memory** (`MEMORY.md` + `USER.md`) with periodic nudges to persist.
- **Autonomous skill creation** — after a complex multi-step task, the agent saves the working procedure as a reusable skill (procedural memory).
- **Skills self-improve during use** — amended when a better path is found.
- **FTS5 cross-session recall** — every past CLI/gateway session is indexed in SQLite and searchable via the `session_search` tool with LLM summarisation.
- **Honcho dialectic user modelling** — optional integration with `plastic-labs/honcho`.
- **Open Skills standard** — compatible with `agentskills.io`; skills are portable and shareable.

### Underlying models

Hermes is **model-agnostic**. It is a *harness*, not a model — no specific weights ship with it. Works with **Nous Portal** (recommended; one subscription, 300+ frontier models), **OpenRouter** (per OpenRouter's own homepage, "400+ active models on 60+ providers"), **OpenAI/Codex/GitHub Copilot**, **Anthropic** (native API key, or Claude Max + extra credits OAuth), **Google Gemini**, **xAI Grok**, **MiniMax, Kimi/Moonshot, z.ai/GLM, Qwen/Alibaba DashScope, DeepSeek, NVIDIA NIM, AWS Bedrock, Hugging Face, Ollama Cloud, NovitaAI, Arcee, GMI Cloud, StepFun, Tencent TokenHub, Xiaomi MiMo, Kilo Code, OpenCode Zen/Go, AI Gateway**, and any self-hosted **Ollama / vLLM / SGLang / llama.cpp / LM Studio / LiteLLM / LocalAI / Jan / ClawRouter** endpoint that speaks OpenAI-compatible REST.

The **Python `AIAgent` default model** is `anthropic/claude-opus-4.6`. Although Nous Research is the lab behind the Hermes 3 / Hermes 4 / Nomos / Psyche model families, the Hermes *Agent* product is intentionally not tied to those weights.

### How it differs from other AI agents

| Dimension | Hermes Agent | Coding copilot | Chatbot wrapper |
|---|---|---|---|
| Host | Server / VPS / cloud sandbox | IDE plugin | Single API + web UI |
| Interfaces | 21+ messaging platforms + CLI + TUI + dashboard + API server + ACP for IDEs | IDE only | Web UI only |
| Memory | Persistent, agent-curated, FTS5 searchable across sessions | Per-conversation | Per-conversation |
| Skills | Agent creates, improves, shares; open standard | None | None |
| Sandboxing | 7 terminal backends (local/Docker/SSH/Daytona/Modal/Singularity/Vercel) | None | None |
| Provider lock-in | None — 30+ providers, `hermes model` to switch | Vendor's | Vendor's |

---

## 2. Setup & Installation

### Prerequisites

- **OS**: Linux, macOS, WSL2 (recommended on Windows), native Windows (early beta), Android via Termux.
- **Python 3.11+** (auto-provisioned by the git installer via `uv`).
- **Git** (the only manual prerequisite for the curl installer).
- Auto-installed: `uv`, Python 3.11, Node.js v22, `ripgrep`, `ffmpeg`.

### Installation paths

**One-line installer (Linux / macOS / WSL2 / Termux):**
```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```
The installer auto-detects Termux and switches to a tested Android flow (`.[termux-all]` extra, fallback to `.[termux]`).

**pip (PyPI release):**
```bash
pip install hermes-agent
hermes postinstall   # optional: installs Node.js, browser, ripgrep, ffmpeg + runs setup
```

**Windows native (PowerShell, early beta):**
```powershell
iex (irm https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.ps1)
```
Bundles PortableGit (~50MB), `uv`, Python 3.11, Node.js 22, ripgrep, ffmpeg under `%LOCALAPPDATA%\hermes`. WSL2 install (`~/.hermes/`) can coexist with native install. **Hermes Desktop** is a thin `.exe` GUI installer that calls `install.ps1` and shares the same dirs.

**From source (contributors):**
```bash
git clone https://github.com/NousResearch/hermes-agent.git
cd hermes-agent
./setup-hermes.sh     # installs uv, creates venv, installs .[all], symlinks ~/.local/bin/hermes
./hermes              # auto-detects the venv
```

**Python library:**
```bash
pip install git+https://github.com/NousResearch/hermes-agent.git
```

**Nix / NixOS** — dedicated flake with declarative module + container mode.

**Docker** — repo ships `Dockerfile` and `docker-compose.yml`. Docker is also one of the terminal *backends* (see below), separately from running Hermes itself in a container.

### Install layout

| Installer | Code | Binary | Data dir |
|---|---|---|---|
| pip | site-packages | `~/.local/bin/hermes` | `~/.hermes/` |
| Per-user git | `~/.hermes/hermes-agent/` | `~/.local/bin/hermes` (symlink) | `~/.hermes/` |
| Root mode | `/usr/local/lib/hermes-agent/` | `/usr/local/bin/hermes` | `/root/.hermes/` or `$HERMES_HOME` |

### Configuration

Two files under `~/.hermes/`:
- **`config.yaml`** — non-secret settings (model, provider, terminal backend, memory limits, compression, skills, display).
- **`.env`** — secrets only (API keys, bot tokens, passwords).

**Precedence** (highest first): CLI args → `config.yaml` → `.env` → built-in defaults.

Recommended CLI router (auto-routes values to the right file):
```bash
hermes config              # view current config
hermes config edit         # open config.yaml in editor
hermes config set KEY VAL  # set a value
hermes model               # interactive provider/model wizard (OAuth + API keys + endpoints)
hermes tools               # configure which tools are enabled per platform
hermes gateway setup       # set up messaging platforms
hermes setup               # full setup wizard
hermes setup --portal      # fast path: Nous Portal OAuth + provider + Tool Gateway in one
```

Environment variable substitution: `${VAR_NAME}` syntax in `config.yaml` (bare `$VAR` not expanded; undefined refs kept verbatim).

### Cloud / sandbox deployment — seven terminal backends

| Backend | Where commands run | Isolation | Best for |
|---|---|---|---|
| `local` | Your machine | None | Personal use |
| `docker` | Single persistent hardened container (`--cap-drop ALL`, `no-new-privileges`, `--pids-limit 256`) | Full | Safe sandboxing, CI/CD |
| `ssh` | Remote server via SSH (ControlMaster reuse, persistent shell on by default) | Network boundary | Remote dev, powerful HW |
| `modal` | Modal cloud sandbox | Full cloud VM | Ephemeral compute, evals |
| `daytona` | Daytona workspace | Full cloud container | Managed cloud dev envs |
| `vercel_sandbox` | Vercel Sandbox microVM | Full | Cloud + snapshot persistence |
| `singularity` | Singularity/Apptainer container | Namespaces | HPC clusters |

**Modal, Daytona, and Vercel Sandbox** support `container_persistent: true` — filesystem hibernates when idle and is snapshotted/restored on next session. The serverless options Nous recommends for an always-on setup with near-zero idle cost.

Files modified inside SSH/Modal/Daytona backends are **automatically synced back to the host** under `~/.hermes/cache/remote-syncs/<session-id>/` on session teardown (cap: `file_sync_max_mb`, default 100 MB).

---

## 3. Core Capabilities & Skills

### Tools (function calling)

The tool registry contains **55 built-in tools** across ~28 toolsets:

- **`terminal`** — `terminal` (shell exec with `background=true` + `notify_on_complete=true`), `process` (manage background processes)
- **`file`** — `read_file` (line-numbered with pagination), `write_file`, `patch` (fuzzy 9-strategy find-and-replace, unified diff, auto-runs syntax checks), `search_files` (ripgrep-backed)
- **`web`** — `web_search`, `web_extract` (markdown + PDF). Backends: Firecrawl, SearXNG, Parallel, Tavily, Exa
- **`browser`** — 12 tools (navigate, click, type, press, scroll, snapshot accessibility tree, get_images, console, back, dialog, cdp raw escape hatch, vision screenshot+AI). Backends: Browserbase cloud, Browser Use cloud, local Chrome/Brave/Chromium/Edge via CDP
- **`vision`** — `vision_analyze`
- **`image_gen`** — `image_generate` (FAL.ai default FLUX 2 Klein 9B; plus FLUX 2 Pro, GPT-Image 1.5/2, Nano Banana Pro, Ideogram V3, Recraft V4 Pro, Qwen, Z-Image Turbo)
- **`tts`** — 10 providers (Edge free, ElevenLabs, OpenAI, MiniMax, Mistral Voxtral, Google Gemini, xAI, NeuTTS, KittenTTS, Piper)
- **`memory`** — `memory` (`add` / `replace` / `remove`; substring matching via `old_text`)
- **`session_search`** — search SQLite FTS5 across all past sessions
- **`skills`** — `skills_list`, `skill_view`, `skill_manage` (create / patch / edit / delete / write_file / remove_file)
- **`delegation`** — `delegate_task` (isolated subagents, parallel execution, only final summary returns)
- **`code_execution`** — `execute_code` (Python script with RPC tool access — "Programmatic Tool Calling", collapses pipelines into one inference turn)
- **`cronjob`** — `cronjob` unified scheduler (create / list / update / pause / resume / run / remove; natural-language schedules, skill attachment)
- **`clarify`** — interactive multiple-choice or freeform user prompt (forces sequential execution)
- **`todo`** — agent-local task list
- **`messaging`** — `send_message` to any connected gateway platform
- **`moa`** — `mixture_of_agents` routes hard problems through 4 reference LLMs + 1 aggregator
- **`homeassistant`** — list_entities / get_state / call_service / list_services
- **`feishu_doc` / `feishu_drive`** — scoped to Feishu document-comment handler
- **`rl`** — 10 tools managing Tinker+WandB RL training runs

**Custom tool integration**: three plugin sources (`~/.hermes/plugins/`, `.hermes/plugins/`, pip entry points) plus MCP.

### MCP (Model Context Protocol)

Hermes is an MCP **client** that loads tools dynamically from any MCP server via stdio or HTTP. Tools appear with a server-name prefix (e.g., `github_create_issue`). Per-server `include` / `exclude` / `resources` / `prompts` filters. Hermes can also be **exposed** as an MCP server via `mcp_serve.py`.

### Memory systems — three layers

**1. Built-in persistent memory** (always on):

| File | Purpose | Char limit |
|---|---|---|
| `MEMORY.md` | Agent's notes — environment, conventions, lessons | 2,200 chars (~800 tokens) |
| `USER.md` | User profile — preferences, comm style, identity | 1,375 chars (~500 tokens) |

Stored under `~/.hermes/memories/`. Loaded as a **frozen snapshot** at session start (preserves prefix cache). Mid-session writes persist to disk immediately but don't appear in the system prompt until next session. Substring matching, automatic duplicate prevention, security-scanned for injection/Unicode tricks before being accepted.

**2. External memory provider plugins** (single-select, plug-in alongside built-in): Honcho (dialectic + multi-agent user modelling), OpenViking, Mem0, Hindsight, Holographic, RetainDB, ByteRover, Supermemory.

**3. Session search** — every session stored in `~/.hermes/state.db` (SQLite + FTS5). `session_search` returns actual messages from past sessions (~20ms FTS5 query, ~1ms scroll). No LLM call. Memory = always-in-context facts (~1,300 tokens fixed cost); session search = on-demand recall.

### Planning & reasoning

- **`todo` tool** intercepted by `AIAgent` directly for complex multi-step tasks.
- **`/reasoning` slash command** — `none` / `minimal` / `low` / `medium` (default unset) / `high` / `xhigh`.
- **Persistent goals (Ralph loop)** — set a standing goal; Hermes works across turns until done.
- **`plan` skill** writes a markdown implementation plan to `.hermes/plans/` instead of executing.

### Multi-agent & orchestration

- **`delegate_task`** — isolated subagents with own conversation, terminal session, toolset. Only final summary returns; intermediate tool results never enter parent context.
- **Two-level orchestration** — `role="orchestrator"` lets children spawn grandchild leaves up to `delegation.max_spawn_depth` (1-3, clamped). At depth 3 with default 3 concurrent children/batch, the tree can reach 3×3×3 = 27 concurrent leaves.
- **Width cap** — `delegation.max_concurrent_children` default 3.
- **Per-child model/provider override** via `delegation.{model, provider, base_url}` — route subagents to cheaper models than parent.
- **Kanban multi-agent** — SQLite-backed task board for coordinating multiple Hermes *profiles*.
- **`execute_code`** — write Python that calls Hermes tools via RPC, collapsing 3+ tool calls + processing logic into one inference turn (massive context savings).

### Scheduled automations

Built-in cron scheduler with natural-language schedules, skill attachment, delivery to any messaging platform. Cron runs in a **fresh session** with no current-chat context. Jobs stored as JSON. Managed via the `cronjob` tool.

### Voice mode

Real-time voice across CLI, Telegram, Discord (DMs, text channels, voice channels). STT: `local` (faster-whisper, free), `groq`, `openai`, `mistral`. Default push-to-talk `Ctrl+B`. Toggle with `/voice on`.

### Skills (procedural memory)

On-demand knowledge documents with **progressive disclosure**:
```
Level 0: skills_list()           → [{name, description, category}, ...]  (~3k tokens)
Level 1: skill_view(name)        → Full SKILL.md content
Level 2: skill_view(name, path)  → Specific reference file
```

All skills live in `~/.hermes/skills/` (with `skills.external_dirs` for shared dirs). Each is a directory with `SKILL.md` (YAML frontmatter + markdown) plus optional `references/`, `templates/`, `scripts/`, `assets/`. Every installed skill is automatically available as `/<skill-name>` in CLI and every gateway platform.

**Skills Hub** integrates with: official optional skills (`optional-skills/` in repo), `skills.sh` (Vercel directory), well-known `/.well-known/skills/index.json` endpoints, direct GitHub repos (default taps `openai/skills`, `anthropics/skills`, `huggingface/skills`, `VoltAgent/awesome-agent-skills`, `garrytan/gstack`), ClawHub, LobeHub, **browse.sh** (200+ site-specific browser-automation skills), Claude marketplace repos, direct HTTPS URLs to single-file SKILL.md.

All hub-installed skills go through a **security scanner** (data exfiltration, prompt injection, destructive commands, supply-chain signals). Trust levels: `builtin` / `official` / `trusted` / `community`. `--force` overrides non-dangerous policy blocks; `dangerous` verdicts stay blocked.

**Skill bundles** — YAML under `~/.hermes/skill-bundles/<slug>.yaml` groups several skills under one slash command.

The repo bundles **~90 skills** by default; **~60 optional skills** are installable via the hub.

---

## 4. Usage & Examples

### CLI

```bash
hermes              # classic CLI (prompt_toolkit)
hermes --tui        # modern Ink TUI (mouse-friendly, modal overlays, non-blocking input)
hermes --continue   # resume most recent session (alias: hermes -c)
hermes chat -q "Summarise this repo"
hermes chat --provider anthropic --model claude-sonnet-4-6
hermes chat --toolsets skills -q "What skills do you have?"
hermes chat --checkpoints   # filesystem snapshots before destructive edits
```

Common slash commands: `/help`, `/tools`, `/model`, `/personality`, `/new`, `/reset`, `/retry`, `/undo`, `/compress`, `/usage`, `/insights [--days N]`, `/skills`, `/<skill-name>`, `/voice on`, `/voice tts`, `/reasoning [level|show|hide]`, `/verbose`, `/save`, `/rollback`, `/stop`, `/quit`.

Multi-line: `Alt+Enter`, `Ctrl+J`, or `Shift+Enter` (Shift+Enter needs Kitty keyboard protocol — Kitty/foot/WezTerm/Ghostty by default; iTerm2/Alacritty/VS Code terminal once Kitty kbd is enabled).

Interrupt: type a new message + Enter, or `Ctrl+C`.

### Messaging gateway

```bash
hermes gateway setup     # interactive platform config
hermes gateway start     # background/foreground
hermes gateway status
hermes gateway run       # foreground (use on WSL2 — systemd unreliable there)
```

Supports **20+ platforms from one gateway process**: Telegram, Discord, Slack, WhatsApp (via Baileys), Signal (via signal-cli), Matrix, Mattermost, Email (IMAP/SMTP), SMS (Twilio), DingTalk, Feishu, WeCom, WeCom callback, Weixin, BlueBubbles, QQBot, Home Assistant, Webhooks, API server, Yuanbao, Microsoft Teams, Google Chat, plus IRC via plugins.

### Python library

```python
from run_agent import AIAgent

# Simple — returns final string
agent = AIAgent(model="anthropic/claude-sonnet-4", quiet_mode=True)
response = agent.chat("What is the capital of France?")

# Full control — returns dict with messages, metadata, usage
result = agent.run_conversation(
    user_message="Search for Python 3.13 features",
    task_id="my-task-1",
)
print(result["final_response"])
```

**Key constructor params:**

| Param | Type | Default | Notes |
|---|---|---|---|
| `model` | `str` | `"anthropic/claude-opus-4.6"` | OpenRouter format |
| `quiet_mode` | `bool` | `False` | **Always `True` when embedding** |
| `enabled_toolsets` | `list[str]` | `None` | Whitelist |
| `disabled_toolsets` | `list[str]` | `None` | Blacklist |
| `save_trajectories` | `bool` | `False` | ShareGPT JSONL |
| `ephemeral_system_prompt` | `str` | `None` | Custom prompt NOT saved to trajectories |
| `max_iterations` | `int` | `90` | Tool-calling cap |
| `skip_context_files` | `bool` | `False` | Skip `AGENTS.md` |
| `skip_memory` | `bool` | `False` | Disable persistent memory r/w |
| `api_key` / `base_url` | `str` | `None` | Override env vars |
| `platform` | `str` | `None` | `"discord"`, `"telegram"`, etc. |

**Thread safety**: create one `AIAgent` per thread/task — state (history, tool sessions, iteration counters) is not safe to share.

### API server

`hermes gateway` can expose Hermes as an **OpenAI-compatible HTTP endpoint** for any frontend speaking the OpenAI API (Open WebUI, LobeChat, LibreChat, …).

### ACP (Agent Context Protocol)

`hermes acp` exposes Hermes as an editor-native agent over stdio/JSON-RPC for **VS Code, Zed, JetBrains**.

### Batch processing

`batch_runner.py` runs the agent across hundreds/thousands of prompts in parallel, generating ShareGPT-format trajectories. Each prompt gets its own `task_id` and isolated environment.

### Example workflows from the docs

- **Daily briefing bot** — cron researches topics + delivers to Telegram/Discord.
- **Team Telegram assistant** — shared bot for the whole team.
- **GitHub PR review agent** — webhook-triggered PR review.
- **Persistent agent on $5 VPS** — talk to it from anywhere via messaging.

---

## 5. Supported Models & Integrations

### Provider catalogue (built-in, first-class)

**OAuth providers**: Nous Portal (subscription, recommended), OpenAI Codex (ChatGPT OAuth), GitHub Copilot (OAuth device code; supports GPT-5.x / Claude / Gemini via Copilot API), GitHub Copilot ACP (spawns local `copilot --acp --stdio`), Anthropic (Claude Max + extra credits OAuth — Claude Pro cannot use this), Google Gemini OAuth (`google-gemini-cli`, free tier supported), Qwen Portal OAuth, MiniMax OAuth, xAI Grok OAuth (SuperGrok / X Premium+).

**API-key providers**: OpenRouter, NovitaAI, Vercel AI Gateway, z.ai/GLM, Kimi/Moonshot (intl + China), Arcee AI, GMI Cloud, MiniMax (global + China), xAI (Responses API), Qwen Cloud / Alibaba DashScope, Alibaba Cloud Coding Plan, Kilo Code, Xiaomi MiMo, Tencent TokenHub, OpenCode Zen, OpenCode Go, DeepSeek, Hugging Face Inference Providers, Google Gemini (API key), LM Studio, NVIDIA NIM, StepFun, Ollama Cloud, **AWS Bedrock** (boto3 credential chain — Claude, Nova, Llama, DeepSeek via Bedrock Converse API).

### Local & self-hosted

Any **OpenAI-compatible** endpoint works:
- **Ollama** (`http://localhost:11434/v1`) — **warning**: defaults to only 4,096 tokens of context on <24GB VRAM. Must set `OLLAMA_CONTEXT_LENGTH=32768` or higher for agent use. Cannot be set via OpenAI-compatible API; must be set server-side.
- **vLLM** — requires `--enable-auto-tool-choice --tool-call-parser <hermes|llama3_json|mistral|deepseek_v3|deepseek_v31|xlam|pythonic>` for tool calling.
- **SGLang** — requires `--tool-call-parser <qwen|llama3|llama4|deepseekv3|mistral|glm>`; defaults to only 128 max output tokens — bump with `--default-max-tokens`.
- **llama.cpp / llama-server** — requires `--jinja` flag for tool calling, else tool calls come back as plain JSON text.
- **LM Studio** — native provider; tool calling introduced in **v0.3.6 (released January 6, 2025)**, per the official LM Studio blog: *"LM Studio 0.3.6 introduces a Function Calling / Tool Use API through LM Studio's OpenAI compatibility API."*
- **LiteLLM proxy, ClawRouter, LocalAI, Jan, Together AI, Groq, Fireworks AI, Cerebras, Mistral AI, Azure OpenAI, Perplexity** — all configurable via `custom_providers:` in `config.yaml`.

### Multi-provider features

- **Fallback providers** — chain of backups tried in order on 429 / 5xx / 401/403. Auxiliary tasks have independent chains.
- **Credential pools** — distribute API calls across multiple keys; strategies `fill_first` (default), `round_robin`, `least_used`, `random`.
- **OpenRouter provider routing** — `sort` (`price` / `throughput` / `latency`), `only:`, `ignore:`, `order:`, `require_parameters:`, `data_collection:`.
- **OpenRouter Pareto Code Router** — `openrouter/pareto-code` auto-routes to cheapest model meeting `openrouter.min_coding_score` (0.0-1.0, default 0.65).

### Auxiliary models

Side tasks (vision, web_extract, approval, compression, skills_hub, mcp, triage_specifier) default to `"auto"` → main chat model. Each can be independently routed to a cheaper/faster model via `auxiliary.<task>.{provider, model, base_url, api_key, timeout}` or interactively via `hermes model` → "Configure auxiliary models".

### Prompt caching

Always-on, no config needed. For Claude on **native Anthropic, OpenRouter, and Nous Portal**, Hermes attaches `cache_control` breakpoints with a **1-hour TTL** (configurable via `prompt_caching.cache_ttl` to `5m`). Qwen Cloud (DashScope) caps TTL at 5 minutes. xAI Grok uses a separate session-pinned `x-grok-conv-id` header mechanism.

---

## 6. Architecture Details

### Top-level structure

The agent's core is a single class, **`AIAgent`**, in `run_agent.py` (15K+ lines). It's the synchronous orchestration engine used by all entry points: CLI (`cli.py`), Gateway (`gateway/run.py`), ACP adapter (`acp_adapter/`), batch runner (`batch_runner.py`), API server (one of the platform adapters), Python library.

Major subsystems:
```
Entry Points → AIAgent
                  ├── Prompt Builder (agent/prompt_builder.py)
                  ├── Provider Resolution (hermes_cli/runtime_provider.py — 18+ providers, OAuth, credential pools)
                  ├── Tool Dispatch (model_tools.py + tools/registry.py — 70+ tools, ~28 toolsets)
                  ├── Compression & Caching (agent/context_compressor.py + agent/prompt_caching.py)
                  ├── 3 API modes: chat_completions / codex_responses / anthropic_messages
                  ├── Session Storage (hermes_state.py — SQLite + FTS5)
                  └── Tool Backends: 7 terminal, 5 browser, 4 web, MCP dynamic, file/vision/etc.
```

### Agent loop (turn lifecycle)

```
run_conversation():
  1. Generate task_id if not provided
  2. Append user message to conversation history
  3. Build or reuse cached system prompt
  4. Check if preflight compression is needed (>50% context)
  5. Build API messages (transcode per API mode)
  6. Inject ephemeral prompt layers (budget warnings, context pressure)
  7. Apply prompt caching markers (Anthropic)
  8. Make interruptible API call
  9. Parse response:
       - If tool_calls: execute, append results, loop back to step 5
       - If text: persist session, flush memory if needed, return
```

**API modes** (resolved from provider/explicit args/base URL heuristics):

| API mode | Used for | Client |
|---|---|---|
| `chat_completions` | OpenAI-compatible (OpenRouter, most providers) | `openai.OpenAI` |
| `codex_responses` | OpenAI Codex / Responses API | `openai.OpenAI` (Responses format) |
| `anthropic_messages` | Native Anthropic Messages API | `anthropic.Anthropic` via adapter |

All three converge on the same internal OpenAI-style message format before/after API calls.

**Strict role alternation** is enforced (User → Assistant → User → …; only `tool` role allowed in consecutive runs). Providers reject malformed histories.

### System prompt structure (slots)

Built by `agent/prompt_builder.py` in this order (verbatim from the prompt-assembly doc):

1. **Agent identity** — `SOUL.md` from `HERMES_HOME` if present, else hardcoded `DEFAULT_AGENT_IDENTITY` fallback. Loaded via `load_soul_md()` which reads `~/.hermes/SOUL.md`, runs a security scan, truncates to 20K chars.
2. **Tool-aware behavior guidance** — memory tool usage, `session_search` guidance, and (for GPT/Codex/Gemini/Gemma/Grok models only) tool-use enforcement clauses like *"You MUST use your tools to take action — do not describe what you would do or plan to do without actually doing it."*
3. **Honcho static block** (when active)
4. **Optional system message**
5. **Frozen MEMORY snapshot** — `MEMORY.md` rendered under `## Persistent Memory` with `[67% — 1,474/2,200 chars]` header and `§` delimiters between entries
6. **Frozen USER profile snapshot** — `USER.md` under `## User Profile`
7. **Skills index** — rendered inside `<available_skills>` grouped by category, with a "Skills (mandatory)" header instructing the model to scan and `skill_view(name)` matching skills
8. **Context files** — first match wins: `.hermes.md`/`HERMES.md` (walks to git root) → `AGENTS.md` (CWD; hierarchical, combines subdirectory AGENTS.md) → `CLAUDE.md` (CWD) → `.cursorrules` / `.cursor/rules/*.mdc` (CWD). SOUL.md skipped here when already loaded in slot 1 (`skip_soul=True`).
9. **Timestamp / optional session ID**
10. **Platform hint** (`"discord"`, `"telegram"`, …)

Each context file is security-scanned for prompt-injection patterns (invisible Unicode, "ignore previous instructions", credential exfiltration), capped at 20,000 chars (70/20 head/tail truncation with marker), YAML frontmatter stripped.

### Cached vs ephemeral layers

Hermes deliberately separates **cached system prompt state** from **ephemeral API-call-time additions**. Items NOT persisted into the cached prefix:
- `ephemeral_system_prompt` (Python param + `HERMES_EPHEMERAL_SYSTEM_PROMPT` env var)
- prefill messages
- gateway-derived session context overlays
- later-turn Honcho recall injected into the current-turn user message

This separation keeps the prefix stable for caching. Memory writes during a session persist to disk immediately but do not mutate the already-built system prompt — they only re-inject at the next session start.

### Prompt caching internals

Anthropic permits max 4 `cache_control` breakpoints; Hermes uses the **`system_and_3`** strategy:

```
Breakpoint 1: System prompt              (stable across all turns)
Breakpoint 2: 3rd-to-last non-system msg  ─┐
Breakpoint 3: 2nd-to-last non-system msg   ├─ Rolling window
Breakpoint 4: Last non-system msg          ─┘
```

`apply_anthropic_cache_control()` deep-copies messages and injects markers `{"type": "ephemeral"}` or `{"type": "ephemeral", "ttl": "1h"}`. Note: "ephemeral" here is Anthropic's marker keyword — unrelated to Hermes' "ephemeral overlay" concept above. Cache invalidation rules:
1. System prompt = breakpoint 1, cached across all turns. Avoid mid-conversation mutation.
2. Message ordering matters — adding/removing mid-stream invalidates everything after.
3. After compression, cache for the compressed region is invalidated but the system prompt cache survives; the rolling 3-message window re-establishes within 1-2 turns.

CLI startup confirms caching: `💾 Prompt caching: ENABLED (Claude via OpenRouter, 5m TTL)`.

### Tool execution

- **Single tool call** → main thread.
- **Multiple tool calls** → concurrent via `ThreadPoolExecutor`. Results reinserted in original order. Interactive tools (`clarify`) force sequential.
- **Flow**: resolve handler → `pre_tool_call` plugin hook → check approval for dangerous commands → execute → `post_tool_call` hook → append `{"role": "tool", "content": result}` to history.
- **Agent-level tools** intercepted by `run_agent.py` *before* the registry: `todo`, `memory`, `session_search`, `delegate_task`. These modify agent state directly and return synthetic results.

### Callback surfaces

`tool_progress_callback`, `thinking_callback`, `reasoning_callback`, `clarify_callback`, `step_callback`, `stream_delta_callback`, `tool_gen_callback`, `status_callback` — enable real-time progress in CLI (spinner), gateway (chat messages), and ACP (editor status).

### Interruptible API calls

API requests run in a background thread; main thread monitors an interrupt event. On interrupt (new user input / `/stop` / signal) the API thread is abandoned, response discarded, no partial response enters history.

### Iteration budget & pressure warnings

- Default `agent.max_turns: 90`. Subagents get independent budgets capped at `delegation.max_iterations: 50`.
- **70% threshold** → `[BUDGET: 63/90. 27 iterations left. Start consolidating.]` injected into the last tool result's JSON.
- **90% threshold** → `[BUDGET WARNING: 81/90. Only 9 left. Respond NOW.]`
- At 100%, agent stops and returns a summary. CLI shows `⚠ Iteration budget reached (90/90) — response may be incomplete`.

### Context compression

**When it triggers:**
- **Preflight** (before API call): >50% of context window (`compression.threshold: 0.50`).
- **Gateway auto-compression**: 85% (more aggressive, between turns).
- **Hygiene hard message limit**: `compression.hygiene_hard_message_limit: 400` — gateway safety valve forcing compression by message count.

**What happens:**
1. Memory flushed to disk first.
2. Phase 1 (cheap): old tool results >200 chars outside the protected tail replaced with `[Old tool output cleared to save context space]`.
3. Middle turns summarised by the auxiliary compression LLM (`auxiliary.compression.*`).
4. Last N messages preserved intact (`compression.protect_last_n: 20`).
5. Tool call/result pairs never split — `_align_boundary_backward()` walks past consecutive tool results to find the parent assistant message.
6. Orphan tool_call/tool_result pairs sanitised by `_sanitize_tool_pairs()`.
7. A new session lineage ID is generated (compression creates a "child" session).

**Context length detection** uses a 9-step chain: config override → custom provider per-model → persistent cache → endpoint `/models` → Anthropic `/v1/models` → OpenRouter API → Nous Portal → **models.dev** registry (per models.dev's own documentation / OpenCode docs: *"OpenCode uses the AI SDK and Models.dev to support 75+ LLM providers"*) → fallback default (128K).

**Pluggable context engines** — `context.engine: "compressor"` (default lossy summarisation) can be replaced by plugin engines like `"lcm"` via `plugins/context_engine/`.

### Session persistence

SQLite (`~/.hermes/state.db`) with FTS5 full-text search. Lineage tracking (parent/child across compressions), per-platform isolation, atomic writes. Resume via `hermes chat --resume`, `/resume`, or `hermes sessions list`.

### Plugin system

Three discovery sources: `~/.hermes/plugins/` (user), `.hermes/plugins/` (project), pip entry points. Plugins register tools, hooks, and CLI commands. Two specialised single-select plugin types: **memory providers** (`plugins/memory/`) and **context engines** (`plugins/context_engine/`).

### Design principles (from architecture doc)

- **Prompt stability** — system prompt doesn't change mid-conversation; no cache-breaking mutations except explicit `/model`.
- **Observable execution** — every tool call visible via callbacks.
- **Interruptible** — API calls + tool execution cancellable mid-flight.
- **Platform-agnostic core** — one `AIAgent` serves CLI, gateway, ACP, batch, API server.
- **Loose coupling** — optional subsystems use registry patterns + `check_fn` gating.
- **Profile isolation** — each profile (`hermes -p <name>`) gets its own `HERMES_HOME`, config, memory, sessions, gateway PID.

---

## 7. Known Limitations & Gotchas

- **Minimum context: 64,000 tokens.** Models with smaller windows are rejected at startup — Hermes' system prompt + tool schemas alone can use 4-8K tokens. For local models, set context ≥64K.
- **Ollama defaults to 4,096 tokens** of context on <24GB VRAM. Must raise via `OLLAMA_CONTEXT_LENGTH=32768` env var, systemd Environment, or a custom Modelfile (`PARAMETER num_ctx 32768`). Cannot be set through OpenAI-compatible API.
- **Native Windows is early beta** — feature parity is mostly there (CLI, gateway, browser, MCP, cron), but the dashboard `/chat` terminal pane is WSL2-only (POSIX PTY). WSL2 is the most battle-tested Windows path.
- **WSL2 + Windows-hosted model server** — `localhost` doesn't bridge by default; need WSL2 mirrored networking mode (Windows 11 22H2+) or explicit Windows host IP + server bound to `0.0.0.0`.
- **WSL2 systemd unreliable** — `hermes gateway start` may not persist across WSL restarts. Use `hermes gateway run` in foreground, tmux, or Windows Task Scheduler.
- **macOS launchd has minimal PATH** — Homebrew, nvm, cargo invisible to gateway. Re-run `hermes gateway install` after installing new tools to re-snapshot PATH.
- **Tool calling on local servers requires explicit flags** — llama.cpp needs `--jinja`, vLLM needs `--enable-auto-tool-choice --tool-call-parser <name>`, SGLang needs `--tool-call-parser <name>`. Without these, tool calls come back as plain JSON text.
- **Anthropic OAuth via `hermes model`** requires a **Claude Max plan + extra usage credits** purchased on top. Claude Pro cannot use this path. Without Max+extra, use an `ANTHROPIC_API_KEY` (pay-per-token).
- **Google Gemini OAuth (`google-gemini-cli`)** uses Google's `gemini-cli` desktop OAuth client. Google considers third-party use a policy violation; some users have reported account restrictions. Hermes shows an upfront warning and requires confirmation. For lowest risk, use the `gemini` provider with your own API key.
- **Memory frozen-snapshot pattern** — mid-session `memory(add)` writes don't appear in the current session's system prompt (preserves prefix cache). Agent sees them via tool responses; they're only re-injected at next session start.
- **Persistent Docker container** — Hermes reuses ONE long-lived container across sessions, `/new`, `/reset`, and `delegate_task` subagents. Parallel subagents share that container — `cd`, env mutation, and writes to the same path collide unless per-task overrides are registered (RL/benchmark envs do this automatically).
- **`container_persistent` only persists filesystem state**, not live PIDs, sandbox identity, or background processes. Modal/Daytona/Vercel hibernation re-creates the sandbox; only snapshotted FS comes back.
- **MCP timeouts** — if an MCP server crashes mid-request, Hermes reports a timeout. Check the server's own logs separately.
- **GitHub Copilot does not support classic PAT** (`ghp_*`). Only `gho_*` (OAuth), `github_pat_*` (fine-grained with Copilot Requests permission), or `ghu_*` (GitHub App) work.
- **Slack channel sessions are keyed by thread** (multi-user shared), while Telegram/Discord channels default to per-user sessions. Configurable via `group_sessions_per_user: false` for shared-room behavior.
- **Hub installs use the GitHub API** — unauthenticated 60 req/hr limit. Set `GITHUB_TOKEN` in `.env` to raise to 5,000 req/hr.
- **`/model` in-session can only switch between providers already configured.** Adding a new provider requires exiting and running `hermes model` from the terminal.
- **Summary model context length** must be ≥ main model's, or summarisation fails and middle turns are dropped without a summary, silently losing context.

### Model requirements for best performance

- 64K+ context window (required).
- Native tool-calling support strongly preferred. The docs list these as having native (best-performance) tool calling: **Llama 3.x, Qwen 2.5 (including Coder), Hermes 2/3, Mistral, DeepSeek, Functionary**. Others use a generic handler that works but may be less efficient.
- Python `AIAgent` defaults to `anthropic/claude-opus-4.6`.
- `agent.tool_use_enforcement` defaults to `"auto"` and automatically injects extra "stop describing intentions, actually call the tool" guidance for models matching substrings `gpt`, `codex`, `gemini`, `gemma`, `grok` — disabled by default for Claude/DeepSeek/Qwen because they use tools reliably without it.

---

## 8. Community & Resources

- **GitHub**: `NousResearch/hermes-agent` — per the GitHub releases page (May 16, 2026), **165k stars, 27.2k forks** ("Fork 27.2k · Star 165k"). 8,000+ commits, MIT license. Languages: ~88% Python, 9% TypeScript. ~3,000+ pytest tests.
- **Releases**: 13 tagged releases; latest **v0.14.0 / `v2026.5.16`** (May 16, 2026).
- **Documentation**: `hermes-agent.nousresearch.com/docs/` — English, 简体中文, 한국어.
- **Machine-readable docs**: `/docs/llms.txt` (~17 KB curated index) and `/docs/llms-full.txt` (~1.8 MB single-file concatenation), regenerated on every deploy, designed for one-shot LLM ingestion.
- **Discord**: `discord.gg/NousResearch` (the main Nous Research server).
- **GitHub Discussions**: `github.com/NousResearch/hermes-agent/discussions`.
- **Issues**: 4.1K open issues, 5K+ PRs.
- **Skills Hub**: `agentskills.io` (open standard) + integrations with `skills.sh`, well-known endpoints, `openai/skills`, `anthropics/skills`, `huggingface/skills`, ClawHub, LobeHub, browse.sh.
- **Related Nous Research projects**:
  - **Hermes 3 / Hermes 4** — Nous's open-weight model families.
  - **Nous Portal** — `portal.nousresearch.com` — unified subscription gateway (300+ models + Tool Gateway for web search / image gen / TTS / cloud browser).
  - **Nous Chat** — `chat.nousresearch.com` — consumer chat using the same subscription.
  - **Nomos** — Nous's optimisation/training stack.
  - **Psyche** — Nous's training framework.
  - **Atropos** — RL training environment integrated with Hermes Agent via the `rl_*` toolset.
- **Community plugins**:
  - **computer-use-linux** (`avifenesh/computer-use-linux`) — Linux desktop-control MCP server (AT-SPI accessibility trees, Wayland/X11 input, screenshots, compositor window targeting).
  - **HermesClaw** (`AaronWong1999/hermesclaw`) — WeChat bridge for running Hermes Agent and OpenClaw on the same WeChat account.
- **OpenClaw migration** — `hermes claw migrate` imports SOUL.md, memories, skills, command allowlist, messaging settings, API keys (allowlisted), TTS assets, workspace instructions.

---

## Quick reference card

```bash
# Install
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash

# First-run wizard (fast path)
hermes setup --portal       # Nous Portal OAuth + provider + Tool Gateway in one
# OR
hermes model                # interactive provider/model wizard
hermes setup                # full wizard

# Day-to-day
hermes                      # classic CLI
hermes --tui                # modern TUI
hermes -c                   # resume last session
hermes gateway start        # messaging gateway
hermes skills search <q>    # Skills Hub
hermes doctor               # diagnose issues
hermes update               # update to latest

# In-session
/model <provider:model>     # switch model
/personality <name>         # switch persona
/compress                   # force context compression
/skills                     # browse skills
/<skill-name>               # invoke skill
/voice on                   # voice mode
/reasoning high             # max reasoning effort
/usage                      # token usage
/insights --days 7          # session analytics
/rollback                   # roll back filesystem
/stop                       # interrupt agent
```

Default model in Python `AIAgent`: **`anthropic/claude-opus-4.6`**. Minimum required context window: **64,000 tokens**. License: **MIT**. Built by **Nous Research**.