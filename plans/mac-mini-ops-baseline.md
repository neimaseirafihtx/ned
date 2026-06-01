# Mac Mini Ops Baseline
*Created 2026-05-29 — updated 2026-06-01 after UGREEN 2.5GbE / HA recovery verification*

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
| LAN adapter | `ifconfig en9` | `2500Base-T <full-duplex>`, active, IP `192.168.68.85` |
| SMB | `nc -vz 127.0.0.1 445` | Port 445 open |

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

## UGREEN 2.5GbE / Home Assistant Recovery Result

Verified 2026-06-01 after moving the Mac Mini's canonical LAN path to the UGREEN USB-C 2.5GbE adapter.

| Item | Result | Notes |
|------|--------|-------|
| Active LAN interface | ✅ `en9` | `192.168.68.85` |
| Adapter MAC | ✅ `6c:1f:f7:c0:3e:e5` | Deco reservation should stay tied to this MAC. |
| Link speed | ✅ `2500Base-T <full-duplex>` | Confirms adapter/cable/switch path negotiated at 2.5GbE. |
| Hostname/mDNS | ✅ `Neimas-Mac-mini.local` | Resolves to `192.168.68.85`. |
| SSH from MBP | ✅ Working | Current session is over SSH from the MBP. |
| SMB | ✅ Working | Local port 445 open; Finder/SMB path should use `smb://192.168.68.85` if mDNS is stale. |
| Home Assistant IP | ✅ HTTP 200 | `http://192.168.68.68:8123/` |
| Home Assistant mDNS | ✅ HTTP 200 | `http://homeassistant.local:8123/` |

Important UTM note: after the adapter swap, the HAOS `Linux` UTM VM must bridge to `en9`, not old `en0`. If HA disappears after a reboot or UTM restart, check live QEMU args for a stale `ifname=en0`, fully quit/reopen UTM, and verify bridge config before assuming HA itself is broken.

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

Canonical script:

```text
scripts/mac-mini-health-check.sh
```

Manual run:

```bash
cd /Users/neimaseirafi/Documents/ned
scripts/mac-mini-health-check.sh
```

It checks:

- Hostname and canonical IP.
- `en9` UGREEN adapter MAC and 2.5GbE link state.
- Hermes gateway.
- Tailscale.
- Ollama API.
- Docker daemon.
- UTM/HAOS caveat: `utmctl` may not work over SSH, so HA HTTP is the real proof.
- Home Assistant via `192.168.68.68` and `homeassistant.local`.
- SMB port 445.
- Root disk and mounted external storage.

Latest manual result: green with one expected SSH-context warning — `utmctl` is not queryable from SSH, but Home Assistant HTTP returned 200 by IP and mDNS.

---

## Daily Hermes Health Brief Cron

Created 2026-06-01.

| Item | Value |
|------|-------|
| Hermes cron job | `7cdc3e9ef531` |
| Name | Daily Mac mini homelab health brief |
| Schedule | `0 8 * * *` — daily at 8:00 AM local Mac Mini time |
| Delivery | Ned Telegram group `telegram:-5158655448` |
| Mode | `no_agent` script-only; stdout is delivered directly |
| Cron wrapper | `/Users/neimaseirafi/.hermes/scripts/mac-mini-health-brief.sh` |
| Repo-owned implementation | `/Users/neimaseirafi/Documents/ned/scripts/mac-mini-health-check.sh` |

Verified test run:

- Last run: `2026-06-01T08:59:01.272859-05:00`
- Status: `ok`
- Delivery error: none reported by Hermes cron
- Next scheduled run: `2026-06-02T08:00:00-05:00`

---

## Status

- [x] First reboot test completed
- [ ] All services verified auto-starting
- [ ] UTM VM auto-start confirmed
- [x] Hermes auto-start confirmed
- [x] Health check script saved on Mac Mini
- [x] Daily Hermes health brief cron created and test-run
- [ ] Remote access from outside home confirmed
