# OpenClaw Research Notes
> Compiled 2026-05-24 for REX setup

---

## What is OpenClaw?

Open-source personal AI agent framework (145k+ GitHub stars). Runs as a background daemon on your machine, connects to messaging platforms (Telegram, Slack, WhatsApp, etc.), executes **skills** on cron schedules, and calls custom TypeScript **tools**.

GitHub: https://github.com/openclaw/openclaw  
Docs: https://docs.openclaw.ai

---

## Installation (on M1 Pro)

**Requirements:** Node 22.19+ (Node 24 recommended)

```bash
npm install -g openclaw@latest
openclaw onboard --install-daemon --anthropic-api-key "sk-ant-YOUR-KEY"
```

Onboarding creates the daemon (launchd on macOS), configures auth, runs health checks.

**Verify:**
```bash
openclaw doctor
openclaw daemon status
```

---

## Key Directories & Files

| Path | Purpose |
|---|---|
| `~/.openclaw/openclaw.json` | Main config: API keys, model, channels, MCP servers |
| `~/.openclaw/workspace/skills/<skill>/` | Skill directory (SKILL.md + index.ts + package.json) |
| `~/.openclaw/cron/jobs.json` | Cron job definitions |

---

## openclaw.json Structure

```json
{
  "env": {
    "ANTHROPIC_API_KEY": "sk-ant-your-key",
    "TAVILY_API_KEY": "tvly-your-key"
  },
  "agents": {
    "defaults": {
      "model": { "primary": "anthropic/claude-sonnet-4-6" },
      "compaction": { "mode": "safeguard" },
      "maxConcurrent": 4,
      "subagents": { "maxConcurrent": 8 }
    }
  },
  "gateway": {
    "mode": "local",
    "bind": "loopback",
    "auth": { "mode": "token" }
  },
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "YOUR_BOT_TOKEN"
    }
  },
  "mcp": {
    "servers": {
      "garmin": {
        "command": "uvx",
        "args": ["garmin-connect-mcp"]
      }
    }
  }
}
```

---

## Skill Directory Structure

```
~/.openclaw/workspace/skills/rex/
├── SKILL.md                # REX brain: persona, goals, reasoning
├── index.ts                # Plugin entry: registers tools with OpenClaw SDK
├── openclaw.plugin.json    # Plugin manifest: declares tool names
├── package.json            # ESM module, OpenClaw compat metadata
├── tsconfig.json
└── tools/
    ├── read_macros.ts
    ├── read_history.ts
    ├── read_context.ts
    ├── save_context.ts
    ├── log_entry.ts
    └── web_search.ts
```

---

## Plugin API (index.ts)

```typescript
import { Type } from "@sinclair/typebox";
import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";

export default definePluginEntry({
  id: "rex",
  name: "REX",
  description: "Daily performance coach",
  register(api) {
    api.registerTool({
      name: "read_macros",
      description: "Reads yesterday's macro entry from macros.jsonl",
      parameters: Type.Object({}),
      async execute(_id, _params) {
        const result = readMacros();
        return { content: [{ type: "text", text: JSON.stringify(result) }] };
      },
    });
    // ... repeat for each tool
  },
});
```

**Key imports:**
```typescript
import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import { Type } from "@sinclair/typebox";
```

---

## openclaw.plugin.json

```json
{
  "id": "rex",
  "name": "REX",
  "description": "Daily performance coaching agent",
  "contracts": {
    "tools": ["read_macros", "read_history", "read_context", "save_context", "log_entry", "web_search"]
  },
  "activation": { "onStartup": true }
}
```

Every tool registered via `api.registerTool()` must also be listed in `contracts.tools`.

---

## package.json (ESM + OpenClaw compat)

```json
{
  "name": "rex-skill",
  "version": "1.0.0",
  "type": "module",
  "openclaw": {
    "extensions": ["./index.ts"],
    "compat": {
      "pluginApi": ">=2026.3.24-beta.2",
      "minGatewayVersion": "2026.3.24-beta.2"
    }
  },
  "scripts": {
    "test": "vitest run",
    "test:watch": "vitest"
  },
  "dependencies": {
    "@sinclair/typebox": "^0.34.0"
  },
  "devDependencies": {
    "typescript": "^5.5.0",
    "vitest": "^2.0.0"
  }
}
```

---

## Cron Setup

Cron jobs are stored in `~/.openclaw/cron/jobs.json`. Add via conversation with the agent:
> "Every morning at 7am, run the rex skill"

Or edit `jobs.json` directly (stop daemon first):
```json
{
  "schedule": "0 7 * * *",
  "action": "run-skill",
  "skillName": "rex"
}
```

Or via CLI (check `openclaw cron --help` for exact syntax):
```bash
openclaw cron add "0 7 * * *" --skill rex
```

---

## Telegram Setup

1. Message @BotFather in Telegram → `/newbot` → get token
2. Add token to `~/.openclaw/openclaw.json` under `channels.telegram.botToken`
3. Restart daemon: `openclaw daemon restart`
4. Message your bot in Telegram, then pair:
   ```bash
   openclaw pairing list telegram
   openclaw pairing approve telegram <CODE>
   ```
5. Verify: `openclaw channels status --probe`

---

## Garmin Connect MCP

**Repo:** https://github.com/eddmann/garmin-connect-mcp  
**Install/auth (requires uv):**
```bash
# Install uv first
curl -LsSf https://astral.sh/uv/install.sh | sh

# Authenticate with Garmin
uvx garmin-connect-mcp auth
# → prompts for Garmin email, password, MFA code
# → saves OAuth tokens to ~/.garminconnect/ (valid ~1 year)
```

**Add to OpenClaw:**
```bash
openclaw mcp set garmin '{"command":"uvx","args":["garmin-connect-mcp"]}'
openclaw daemon restart
```

**22 tools exposed** — HRV, sleep, Body Battery, RHR, activities, training load, VO2 max, recovery time, SpO2, stress, weight, and more.

---

## Testing Plugins

```bash
# Inspect plugin runtime (must be deployed to ~/.openclaw/workspace/skills/rex/)
openclaw plugins inspect rex --runtime --json
```

---

## Useful Commands

```bash
openclaw doctor                     # Health check
openclaw daemon restart             # Restart gateway
openclaw models list                # List available models
openclaw channels status --probe    # Check channel connections
openclaw mcp list                   # List configured MCP servers
openclaw plugins list               # List installed skills
openclaw tui                        # Terminal UI
openclaw dashboard                  # Web dashboard (localhost:18789)
```
