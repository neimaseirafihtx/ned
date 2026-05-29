---
name: macbook-m5pro
description: Neima's MBP M5 Pro — primary workstation and current AI experimentation machine with Hermes Agent + Ollama
metadata:
  type: user
---

MacBook Pro M5 Pro — primary workstation and current AI experimentation hub. Not a permanent server.

- **Chip:** Apple M5 Pro, 20-core GPU
- **RAM:** 48GB unified memory
- **Storage:** 1TB SSD
- **OS:** macOS

**AI agent stack:**
- **Hermes Agent** running — GPT-5.5 (OpenAI) as backend ✅
- Hermes moves to Mac Mini once it arrives; MBP stays as dev/experimentation machine

**Local LLM stack:**
- Ollama installed — `qwen3.6:27b-mlx` and `qwen3.6:36b`
- Open WebUI running on localhost:8080
- Confirmed stable under full load: Ollama at 24.76GB, 0 swap, green memory pressure

**Active use case for local models: none.** Claude + Claude Code cover primary work. Hermes uses GPT-5.5. Mac Mini 8B handles HA automation. Local Ollama on MBP has no gap to fill in current workflow — kept for privacy-sensitive edge cases and experimentation only. Don't suggest local MBP models as a solution unless the use case is offline or privacy-critical.
