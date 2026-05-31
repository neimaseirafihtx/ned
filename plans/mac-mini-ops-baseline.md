# Mac Mini Ops Baseline
*Created 2026-05-29 — updated 2026-05-31 after first full reboot test*

---

## Purpose

Verify the Mac Mini is boring and reliable before building agent workflows on top of it. If the base host is flaky, every future agent workflow becomes fragile.

---

## Reboot Checklist

After every Mac Mini reboot, verify:

| Service | How to check | Expected |
|---------|-------------|----------|
| Tailscale | `tailscale status` | Connected, `neima.seirafi@gmail.com` tailnet |
| HAOS VM | `curl -I http://homeassistant.local:8123` | HA returns HTTP 200/login page |
| Ollama | `ollama list` | qwen3.5:9b listed |
| Docker | `docker ps` | No daemon error |
| Hermes Agent | Telegram message → response | Hermes replies |
| SSH from MBP | `ssh mac-mini` | Connects without password |
| Remote (Tailscale) | SSH from outside network | Connects via Tailscale IP |

---

## First Reboot Test Result

Completed during Phase 3 activation work.

| Service | Result | Notes |
|---------|--------|-------|
| Hermes gateway | ✅ Auto-started | Telegram/Hermes path survived reboot. |
| Tailscale | ✅ Auto-started | Launchd-backed daemon came back normally. |
| Ollama | ✅ Auto-started | Homebrew service came back normally. |
| Docker Desktop | ⚠️ Manual start needed | `docker ps` failed until Docker Desktop was opened with `open -a Docker`. |
| HAOS / Home Assistant UTM VM | ⚠️ Manual start needed | UTM VM is named `Linux`; `utmctl start 'Linux'` was needed before `homeassistant.local:8123` returned 200. |

Operational takeaway: Hermes/Tailscale/Ollama are stable after reboot; Docker Desktop and HAOS VM need explicit startup handling before the Mac Mini is fully boring.

---

## Service Startup State

| Service | Auto-starts? | How / current action |
|---------|-------------|----------------------|
| Tailscale | ✅ | `tailscaled install-system-daemon` — launchd |
| HAOS (UTM VM) | ⚠️ No / not reliable yet | Start manually with `utmctl start 'Linux'`; later automate via Login Item/LaunchAgent if needed. |
| Ollama | ✅ | `brew services start ollama` — launchd |
| Docker | ⚠️ No / not reliable yet | Start Docker Desktop with `open -a Docker`; later verify Login Item or replace with a more server-native Docker runtime if needed. |
| Hermes Agent | ✅ | Gateway survived reboot in the first test. |

Known gaps:
- Make HAOS VM startup automatic or intentionally document it as manual.
- Make Docker startup automatic or document `open -a Docker` as the runbook step.
- Confirm remote SSH from outside the home network via Tailscale when off LAN.

---

## Health Check Script

```bash
#!/bin/bash
echo "=== Mac Mini Health ==="
echo "Tailscale: $(tailscale status | head -1)"
echo "Ollama: $(ollama list 2>/dev/null | grep qwen || echo 'NOT RUNNING')"
echo "Docker: $(docker ps -q 2>/dev/null | wc -l | tr -d ' ') containers running"
echo "HA: $(curl -s -o /dev/null -w '%{http_code}' http://homeassistant.local:8123)"
echo "Disk: $(df -h / | tail -1 | awk '{print $4}') free"
```

Save as `~/scripts/health-check.sh`, run after reboots, and reuse the same checks for the first daily Hermes health brief.

---

## Status

- [x] First reboot test completed
- [ ] All services verified auto-starting
- [ ] UTM VM auto-start confirmed
- [x] Hermes auto-start confirmed
- [ ] Health check script saved on Mac Mini
- [ ] Remote access from outside home confirmed
