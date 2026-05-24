---
name: macbook-m5pro
description: Neima's personal MacBook Pro M5 Pro specs and locally installed LLM stack
metadata:
  type: user
---

MacBook Pro M5 Pro — personal laptop, not a server.

- **Chip:** Apple M5 Pro, 20-core GPU
- **RAM:** 48GB unified memory
- **Storage:** 1TB SSD
- **OS:** macOS

**Local LLM stack:**
- Ollama installed
- Models: `qwen3:6-27b-mlx` (MLX-native, Apple Silicon optimized) and `qwen3.6:36b`
- Open WebUI running locally

**Notes:** The 27B MLX variant is Apple Silicon-native (Neural Engine + GPU) — lower latency than standard GGUF. 36B at Q4 is ~20-22GB, fits comfortably in 48GB. Open WebUI can connect to multiple Ollama backends (e.g., Mac Mini via Tailscale) for a unified interface across machines.
