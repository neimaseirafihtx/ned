# Local LLM Models — Hardware Tiers & Recommendations

Last updated: 2026-05-31

## Hardware Tiers

### Mac Mini M4 — 16GB (Neima's current server)

**What fits comfortably:**
- `llama3.1:8b` — fast, capable, good for automation calls
- `qwen2.5:7b` — surprisingly good coder, fast
- `mistral:7b` — solid all-rounder
- `phi3.5:3.8b` — very fast, minimal RAM, great for HA automation

**What fits but is slow:**
- `qwen2.5:14b` — fits in 16GB with quantization (Q4), usable but slower
- `llama3.1:13b` — similar story

**What does NOT fit:**
- Any 32B+ model — needs 20GB+ even at Q4. Don't try it, you'll swap to disk and hate life.
- `llama3.1:70b` — needs ~40GB minimum

**Recommended for Home Assistant automation calls:** `llama3.1:8b` or `phi3.5:3.8b`
- Speed matters more than raw quality here — HA needs fast responses
- These models handle structured JSON output reliably enough for automation
- Phi3.5 at 3.8B is shockingly capable for its size

**Recommended for general chat/coding on 16GB:** `qwen2.5:14b:q4_K_M`
- Best quality that actually fits
- Noticeably better at code than llama 8B

### Mac Mini M4 — 24GB (upgrade path)

Opens up `qwen2.5:14b` at full Q6/Q8 quality, and `mistral-small` (24B) comfortably.

### Mac Mini M4 Pro — 24GB or 48GB

- 24GB: `qwen2.5:14b` great, some 24B models at Q5/Q6
- 48GB: `llama3.3:70b` at Q4 — this is where local LLMs start feeling genuinely impressive

### Windows RTX Desktop (Neima's future build)

GPU VRAM is the constraint, not system RAM.

- RTX 4070 (12GB VRAM): `llama3.1:8b` fast, `qwen2.5:14b` at Q4 fits
- RTX 4080 (16GB VRAM): `qwen2.5:14b` full quality, some 24B at Q4
- RTX 4090 (24GB VRAM): `llama3.3:70b` at Q4 with good speed
- RTX 5090 (32GB VRAM): nearly anything at Q4/Q5

GPU inference (CUDA) is 3-5x faster than Apple Silicon for the same model size.

## Ollama Quickstart

```bash
# Install
brew install ollama

# Run as service (starts on boot)
brew services start ollama

# Pull a model
ollama pull llama3.1:8b

# Run interactive
ollama run llama3.1:8b

# API (same port as OpenAI-compatible)
curl http://localhost:11434/api/generate \
  -d '{"model":"llama3.1:8b","prompt":"Hello"}'
```

**OpenAI-compatible API endpoint:** `http://localhost:11434/v1`
This means any app that supports "custom OpenAI base URL" can point at Ollama.

## OpenWebUI

Best local chat UI for Ollama. Docker one-liner:

```bash
docker run -d \
  --name open-webui \
  -p 3000:8080 \
  -v open-webui:/app/backend/data \
  --add-host=host.docker.internal:host-gateway \
  ghcr.io/open-webui/open-webui:main
```

Then: http://localhost:3000

## Honest Quality Assessment

Local LLMs have gotten genuinely good, but be realistic:

| Task | Local LLM (8B-14B) | Claude |
|------|-------------------|--------|
| Simple automation (JSON output) | ✅ Good enough | Overkill |
| Code generation (medium complexity) | ⚠️ Hit or miss | Much better |
| Complex reasoning / analysis | ❌ Falls apart | Strong |
| Long context (>8K tokens) | ⚠️ Degrades | Handles well |
| Following complex instructions | ⚠️ Inconsistent | Reliable |

**Bottom line for Neima's setup:** Local LLMs are great for HA automation calls, quick summaries, and keeping data local. Don't try to replace Claude for anything requiring real reasoning. That's not a knock on Ollama — it's just using the right tool.

## Cloud + Local Routing Strategy

Current subscription posture:
- **Hermes/OpenAI via ChatGPT OAuth** is the primary always-on Ned operator while the $20 subscription path remains low-friction and cost-effective.
- **Claude subscription** is the second-brain lane for planning, architecture, long-context docs, code review, and careful critique.
- **Grok/xAI OAuth** is a possible cloud contingency lane if Hermes support becomes stable enough for day-to-day use.
- **Local Ollama/llama.cpp models** are supporting workers for simple summaries, log triage, structured extraction, Home Assistant intent parsing, privacy-sensitive prompts, and offline fallback.

Routing rule of thumb:
- Use cloud for anything that needs real judgment, long context, tool orchestration, Git/repo updates, or infrastructure safety.
- Use Claude when a second opinion, writing quality, architectural review, or code review matters.
- Use Grok/xAI as a contingency cloud provider if OAuth access through Hermes is stable and quality is good enough for the task.
- Use local models when speed/privacy/offline availability matters more than top-tier reasoning.
- Do not treat local models as the primary Ned replacement until they can pass real workflow tests on the Mac Mini and MacBook Pro.

## Home Assistant Integration

Two good options:

**1. Extended OpenAI Conversation (recommended)**
- Install via HACS
- Points at Ollama's OpenAI-compatible endpoint: `http://<mac-mini-ip>:11434/v1`
- Use `llama3.1:8b` or `phi3.5:3.8b`
- Fast enough for voice assistant response times

**2. Ollama Integration (native)**
- Built into recent HA versions
- Simpler setup, slightly less flexible

**Recommended system prompt for HA automation:**
```
You are a smart home assistant. Respond ONLY with valid JSON for the requested action.
Never add explanation or markdown. Available entities: [list them here]
```

## Model Release Cadence

This space moves fast. Check:
- https://ollama.com/library — what's available to pull
- https://huggingface.co/spaces/lmsys/chatbot-arena-leaderboard — benchmarks
- New Llama/Qwen/Mistral releases drop every few months with meaningful improvements
