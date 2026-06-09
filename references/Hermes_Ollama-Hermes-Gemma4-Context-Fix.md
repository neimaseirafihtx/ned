# Hermes + Ollama Gemma4:12B on Windows

Date documented: 2026-06-08 22:29 CDT
Host: `NEIMA_SERVER` / `Neima_Server`
Repo path: `C:\Users\neima\Documents\ned`
Hermes home: `C:\Users\neima\AppData\Local\hermes`

## Current known-good state

Hermes has two relevant profiles on the Windows PowerSpec host:

| Profile | Purpose | Provider | Model | Base URL | Gateway |
|---|---|---|---|---|---|
| `default` | Main Ned / Telegram profile | `openai-codex` | `gpt-5.5` | empty | running |
| `ha-local` | Local Ollama test/profile | `custom` | `Gemma4:12B` | `http://localhost:11434/v1` | stopped |

The local profile works through Hermes against Ollama's OpenAI-compatible endpoint.

Verified commands:

```bash
hermes profile list
ollama list
ollama ps
hermes -p ha-local config
hermes -p ha-local chat -q 'Reply with exactly: local model ready' --toolsets safe --quiet
hermes -p ha-local chat -q 'Use the terminal tool to run: printf "tool-ok". Then reply with exactly the command output and nothing else.' --toolsets terminal --quiet
```

Verified results:

```text
ha-local        Gemma4:12B                   stopped

NAME          ID              SIZE      MODIFIED
Gemma4:12B    4eb23ef187e2    7.6 GB    ...

NAME          ID              SIZE      PROCESSOR    CONTEXT
Gemma4:12B    4eb23ef187e2    8.4 GB    100% GPU     32768

local model ready
tool-ok
```

## Hermes config settings

### Default profile

Path:

```text
C:\Users\neima\AppData\Local\hermes\config.yaml
```

Model block:

```yaml
model:
  default: gpt-5.5
  provider: openai-codex
  base_url: ''
```

This is intentional: the main Ned profile remains OpenAI Codex GPT-5.5.

### Local Ollama profile: `ha-local`

Path:

```text
C:\Users\neima\AppData\Local\hermes\profiles\ha-local\config.yaml
```

Known-good model block:

```yaml
model:
  default: Gemma4:12B
  provider: custom
  base_url: http://localhost:11434/v1
```

Important details:

- Use `provider: custom`, not `provider: ollama`.
- Use Ollama's OpenAI-compatible endpoint: `http://localhost:11434/v1`.
- Use the exact installed model name from `ollama list` / `/v1/models`.
- In this setup, the installed model name is case-sensitive as exposed by Ollama: `Gemma4:12B`.

## Error 1: too-small context window caused Hermes truncation failure

### Symptom

Hermes failed even on a tiny prompt like `hi`.

Visible error:

```text
Error: Response remained truncated after 3 continuation attempts
```

Hermes then tried continuation prompts like:

```text
[System: Your previous response was truncated by the output length limit. Continue exactly where you left off. Do not restart or repeat prior text. Finish the answer directly.]
```

### Root cause

Ollama had loaded the model with only a `4096` token active context window.

That is too small for full Hermes agent mode because Hermes sends a large startup prompt containing:

- persona and operating rules
- memory / user profile context
- tool schemas
- skills-routing instructions
- execution and safety rules

With only 4096 tokens, the prompt consumed nearly the entire model context and left essentially no room for an answer.

Observed failure pattern:

```text
prompt_tokens=4095
completion_tokens=1
total_tokens=4096
finish_reason='length'
```

The local model was not incapable of answering. The active context window was too small.

### Diagnostic proof

Check active loaded context:

```bash
ollama ps
```

Bad state:

```text
CONTEXT
4096
```

Good state:

```text
CONTEXT
32768
```

This matters because config files alone do not prove the loaded model is using the desired context. An already-loaded Ollama model can remain at the old context until the Ollama server/model is fully restarted and reloaded.

### Fix: restart Ollama with larger active context

On Windows, quit Ollama completely from the tray:

1. Look near the Windows clock.
2. Right-click the Ollama llama icon.
3. Click **Quit Ollama**.

If Ollama refuses to stop or the port remains busy, PowerShell fallback:

```powershell
taskkill /IM ollama.exe /F
taskkill /IM "ollama app.exe" /F
taskkill /IM llama-server.exe /F
```

Start Ollama with a larger context window:

```powershell
$env:OLLAMA_CONTEXT_LENGTH="32768"
ollama serve
```

Leave that PowerShell window open.

In another terminal, force-load the model and verify context:

```powershell
ollama run Gemma4:12B "hi"
ollama ps
```

Expected:

```text
CONTEXT
32768
```

Then test Hermes again:

```powershell
hermes -p ha-local chat -q "hi" -Q
```

### Make the context setting persistent

The temporary PowerShell environment variable only applies to that process. To persist for the current Windows user:

```powershell
setx OLLAMA_CONTEXT_LENGTH 32768
```

Then fully quit and restart Ollama again.

After restart, verify again:

```powershell
ollama run Gemma4:12B "hi"
ollama ps
```

Do not assume persistence worked until `ollama ps` shows `32768` in the `CONTEXT` column.

## Error 2: Hermes profile pointed at the wrong model name

### Symptom

The first `ha-local` Hermes test failed with:

```text
API call failed after 3 retries: HTTP 404: model 'gemma4:e4b' not found
```

### Root cause

`ha-local` was configured with:

```yaml
model:
  default: gemma4:e4b
```

But Ollama exposed the installed model as:

```text
Gemma4:12B
```

Confirmed via:

```bash
ollama list
curl -s http://localhost:11434/v1/models
```

`/v1/models` returned:

```json
{"object":"list","data":[{"id":"Gemma4:12B","object":"model","owned_by":"library"}]}
```

### Fix

Set the exact model name in the Hermes profile:

```bash
hermes -p ha-local config set model.default Gemma4:12B
```

Retest:

```bash
hermes -p ha-local chat -q 'Reply with exactly: local model ready' --toolsets safe --quiet
```

Expected:

```text
local model ready
```

## Config migration we ran

`ha-local` initially had an outdated config version:

```text
Config version outdated (v24 → v28)
```

We ran:

```bash
hermes -p ha-local doctor --fix
```

It migrated the profile config to v28 and lowered `model_catalog.ttl_hours` to `1`.

Verification after migration:

```bash
hermes -p ha-local doctor
hermes -p ha-local chat -q 'Reply with exactly: migrated config still works' --toolsets safe --quiet
```

Expected:

```text
Config version up to date (v28)
migrated config still works
```

## Smoke-test checklist

Use this when validating local Hermes/Ollama again.

### 1. Verify Ollama is serving the model

```bash
ollama list
ollama ps
curl -s http://localhost:11434/v1/models
```

Look for:

```text
Gemma4:12B
CONTEXT 32768
```

### 2. Verify Hermes profile config

```bash
hermes -p ha-local config
```

Look for:

```text
{'default': 'Gemma4:12B', 'provider': 'custom', 'base_url': 'http://localhost:11434/v1'}
```

### 3. Safe model response test

```bash
hermes -p ha-local chat -q 'Reply with exactly: local model ready' --toolsets safe --quiet
```

Expected:

```text
local model ready
```

### 4. Tool-calling test

```bash
hermes -p ha-local chat -q 'Use the terminal tool to run: printf "tool-ok". Then reply with exactly the command output and nothing else.' --toolsets terminal --quiet
```

Expected:

```text
tool-ok
```

### 5. Response sanity test

```bash
hermes -p ha-local chat -q 'Answer in exactly three bullets: what does a Hermes profile with provider custom and base_url http://localhost:11434/v1 mean? Keep it factual.' --toolsets safe --quiet
```

The verified answer correctly stated that:

- `custom` tells Hermes to use a direct endpoint rather than a built-in cloud provider integration.
- `http://localhost:11434/v1` is Ollama's local OpenAI-compatible API endpoint.
- Hermes is talking to a locally hosted model through OpenAI-compatible request/response format.

## Current caveats

- `ha-local` gateway is stopped. The running gateway is the `default` profile.
- Main Ned Telegram still uses the default OpenAI Codex GPT-5.5 profile unless the gateway/profile setup is changed.
- `homeassistant` toolset is not yet available in `ha-local`; doctor reports missing system dependency/config. The local model profile works, but this is not yet a working Home Assistant-control profile.
- Missing API key warnings from `hermes -p ha-local doctor` are expected if the profile is intended to stay mostly local.

## Key lesson

For Hermes + Ollama troubleshooting, verify runtime state, not just config.

The minimum proof is:

```bash
ollama ps
hermes -p ha-local config
hermes -p ha-local chat -q 'Reply with exactly: local model ready' --toolsets safe --quiet
```

A config that looks right is not enough. The Ollama model must be actively loaded with enough context, and Hermes must be using the exact model name Ollama exposes.
