# Mac Mini Ops Baseline
*Created 2026-05-29 — complete after first full reboot test*

---

## Purpose

Verify the Mac Mini is boring and reliable before building agent workflows on top of it. If the base host is flaky, every future agent workflow becomes fragile.

---

## Reboot Checklist

After every Mac Mini reboot, verify:

| Service | How to check | Expected |
|---------|-------------|----------|
| Tailscale | `tailscale status` | Connected, `neima.seirafi@gmail.com` tailnet |
| HAOS VM | `http://homeassistant.local:8123` | HA login page loads |
| Ollama | `ollama list` | qwen3.5:9b listed |
| Docker | `docker ps` | No errors |
| Hermes Agent | Telegram message → response | Hermes replies |
| SSH from MBP | `ssh mac-mini` | Connects without password |
| Remote (Tailscale) | SSH from outside network | Connects via Tailscale IP |

---

## Service Startup State

| Service | Auto-starts? | How |
|---------|-------------|-----|
| Tailscale | ✅ | `tailscaled install-system-daemon` — launchd |
| HAOS (UTM VM) | ⚠️ TBD | UTM needs to auto-start VM on login |
| Ollama | ✅ | `brew services start ollama` — launchd |
| Docker | ✅ | Docker Desktop login item |
| Hermes Agent | ⚠️ TBD | Verify after reboot |

**Known gap:** UTM VM auto-start on login not yet confirmed. Set up via:
```bash
utmctl start "Home Assistant"
```
Or add UTM to Login Items and configure VM to auto-start.

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

Save as `~/scripts/health-check.sh`, run after reboots.

---

## Status

- [ ] First reboot test completed
- [ ] All services verified auto-starting
- [ ] UTM VM auto-start confirmed
- [ ] Hermes auto-start confirmed
- [ ] Health check script saved on Mac Mini
- [ ] Remote access from outside home confirmed
