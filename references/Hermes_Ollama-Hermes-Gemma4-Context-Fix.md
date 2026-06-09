# Ollama + Hermes Gemma4 Context Window Fix

Date documented: 2026-06-08 09:44:29 CDT

## Summary

Hermes was failing on the local Ollama `gemma4:12b` model even for a tiny prompt like `hi`.

The visible symptom was:

```text
Error: Response remained truncated after 3 continuation attempts
```

The root cause was not that Gemma could not answer. The root cause was that Ollama had loaded `gemma4:12b` with only a **4096-token context window**, while full Hermes agent mode sends a large startup prompt containing persona, memories, rules, and tool descriptions. That startup prompt filled the model context before the model had room to answer.

After restarting Ollama with `OLLAMA_CONTEXT_LENGTH=32768`, the model loaded with a large enough active context and Hermes was able to answer normally.

---

## What we tested and observed

### 1. Full Hermes local model call failed

We tested a minimal Hermes prompt:

```bash
hermes chat -q 'hi' -Q
```

It failed with:

```text
Error: Response remained truncated after 3 continuation attempts
```

This looked like a truncation/continuation bug because Hermes kept injecting a continuation system message similar to:

```text
[System: Your previous response was truncated by the output length limit. Continue exactly where you left off. Do not restart or repeat prior text. Finish the answer directly.]
```

### 2. Direct/simple Hermes isolation worked

We tested a reduced Hermes prompt without the full rules/tool load:

```bash
hermes chat -q 'hi' --ignore-rules -t terminal -Q
```

That worked and returned:

```text
Hello! How can I help you today?
```

This proved the local Gemma model could answer a simple prompt, and the failure was specific to the full Hermes agent prompt size/context behavior.

### 3. Ollama showed the model loaded with only 4096 context

We checked the loaded Ollama model state:

```bash
ollama ps
```

The important part was the `CONTEXT` column:

```text
NAME          ... CONTEXT
 gemma4:12b   ... 4096
```

That confirmed the model was actively running with a 4096-token context window.

### 4. Hermes debug output showed context exhaustion

The failure pattern was consistent with:

```text
prompt_tokens=4095
completion_tokens=1
total_tokens=4096
finish_reason='length'
```

Meaning: the prompt alone consumed essentially the entire model context, so Ollama stopped immediately with a length finish reason.

---

## Fix we applied

### Step 1: Quit Ollama completely

From Windows, quit Ollama from the system tray:

1. Look near the Windows clock.
2. Right-click the Ollama llama icon.
3. Click **Quit Ollama**.

If Ollama refuses to stop or the port remains busy, use PowerShell:

```powershell
taskkill /IM ollama.exe /F
taskkill /IM "ollama app.exe" /F
taskkill /IM llama-server.exe /F
```

### Step 2: Start Ollama with a larger context window

Open PowerShell and run:

```powershell
$env:OLLAMA_CONTEXT_LENGTH="32768"
ollama serve
```

Leave that PowerShell window open. It is now running the Ollama server with the larger context setting.

### Step 3: Load/test Gemma in another terminal

Open a second PowerShell window and run:

```powershell
ollama run gemma4:12b "hi"
```

This forces Ollama to load `gemma4:12b` under the new server environment.

### Step 4: Verify the active context window

In the second terminal, run:

```powershell
ollama ps
```

Before the fix, the `CONTEXT` column showed:

```text
4096
```

After the fix, it should show:

```text
32768
```

This verification matters because Hermes/Ollama config values alone are not enough. An already-loaded Ollama model may remain at the old context size until the server/model is restarted and reloaded.

### Step 5: Test Hermes again

Run:

```powershell
hermes chat -q "hi" -Q
```

After the Ollama restart/context fix, this worked.

---

## Optional: make the context setting persistent

The PowerShell `$env:OLLAMA_CONTEXT_LENGTH="32768"` setting only applies to the current terminal/session.

To make the setting persistent for the current Windows user, run:

```powershell
setx OLLAMA_CONTEXT_LENGTH 32768
```

Then fully quit and restart Ollama again.

Recommended verification after restart:

```powershell
ollama run gemma4:12b "hi"
ollama ps
```

Confirm `CONTEXT` is still:

```text
32768
```

---

## Why this fixed Hermes

Hermes full agent mode includes a large system prompt with:

- persona/instructions
- persistent memory
- available tool descriptions
- skill-routing instructions
- safety/execution rules

That prompt can be much larger than a normal chat prompt. With Ollama's default 4096-token active context, the prompt left almost no room for the model response. Ollama therefore returned a `length` finish reason immediately, which Hermes interpreted as a truncated response and tried to continue repeatedly.

Increasing Ollama's active context to 32768 gave the model enough room for the Hermes prompt plus the reply.

---

## Important diagnostic commands

Check loaded models and active context:

```powershell
ollama ps
```

Check installed models:

```powershell
ollama list
```

Run a direct model smoke test:

```powershell
ollama run gemma4:12b "hi"
```

Run a full Hermes smoke test:

```powershell
hermes chat -q "hi" -Q
```

Run a reduced Hermes isolation probe:

```powershell
hermes chat -q "hi" --ignore-rules -t terminal -Q
```

---

## Key lesson

For Hermes + Ollama debugging, do not trust only the configured context values. Always verify the **active loaded model context** with:

```powershell
ollama ps
```

If it shows `4096`, full Hermes agent mode may fail even on tiny prompts.

The fix is to restart/reload Ollama with a larger `OLLAMA_CONTEXT_LENGTH`, then verify that `ollama ps` shows the larger context.
