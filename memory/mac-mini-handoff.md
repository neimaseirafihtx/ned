# Mac Mini M4 — Setup Handoff
*Generated 2026-05-28*

---

## What's Done ✅

### Physical Setup
- Mac Mini M4 (16GB) arrived and connected via ethernet
- Confirmed ~1Gbps up/down, 1ms ping on speedtest — wired, line rate on AT&T Fiber

### macOS Configuration
- **Apple ID signed in** — iCloud selectively configured (see below)
- **iCloud ON:** iCloud Drive, Keychain, Notes, Messages, Mail, Find My, Contacts, Calendar, Reminders, Safari
- **iCloud OFF:** Photos, FaceTime, Freeform, Siri, Wallet, Home
- **FileVault** — was on, fully decrypted and left off for headless/home-server recoverability
- **Energy settings:**
  - Prevent automatic sleeping when display is off → ON
  - Wake for network access → ON
  - Start up automatically after power failure → ON
- **macOS version:** macOS Tahoe 26.5 (updated from 26.4 — Screen Sharing auth was broken on 26.4, fixed in 26.5)
- **Sharing settings:**
  - Remote Login → ON
  - Remote Management → OFF
  - File Sharing → ON, hardened for authenticated SMB access to `Neima Home Folder`; guest SMB access disabled
  - Screen Sharing → ON ✅
    - Anyone may request permission: Off
    - VNC viewers may control screen with password: Off
    - Allow access for: Neima Seirafi only
- **Note:** older launchctl commands (`launchctl load`) don't work on macOS Tahoe 26, use `launchctl enable` + `kickstart`

### Remote Access
- SSH working from MBP → Mac Mini ✅
- SSH key auth set up — no password required ✅
- Alias configured on MBP: type `mac-mini` to connect instantly ✅
- Static IP `192.168.68.85` reserved in router ✅
- Automatic login enabled ✅
- Mac Mini username: `neimaseirafi`
- Hostname: `Neimas-Mac-mini.local`

---

## What's Left 📋

### Immediate (do next session)

1. ~~**Homebrew**~~ ✅ already installed
2. ~~**Tailscale**~~ ✅ installed and authenticated — `neima.seirafi@gmail.com` tailnet, daemon registered via `tailscaled install-system-daemon`

### Phase 2 Infrastructure (after foundation)

5. ~~**Docker**~~ ✅ Docker Desktop installed and running (ARM native, no Rosetta)

6. ~~**UTM + Home Assistant OS VM**~~ ✅ HAOS 17.3 running in UTM VM, accessible at homeassistant.local:8123

7. ~~**Ollama (8B/9B-class model)**~~ ✅ installed and running with `qwen3.5:9b`
   - For HA automation and light local use only — not heavy general inference
   - 16GB RAM is tight; heavy inference stays off this box

8. **Nextcloud**
   - Personal data layer agents can operate on
   - Samsung T9 1TB SSD (planned) as storage backend

9. ~~**Hermes Agent migration**~~ ✅ Hermes Agent running on Mac Mini — GPT-5.5 backend, Telegram connected

---

## Reference

| Item | Value |
|------|-------|
| Mac Mini username | `neimaseirafi` |
| Hostname | `Neimas-Mac-mini.local` |
| SSH alias (MBP) | `mac-mini` |
| Static IP | `192.168.68.85` |
| Vet (Coco) | Meredith Perry DVM, Montrose Vet, 713-524-3814 |

---

## Roadmap Context

AI mastery is the primary goal. Mac Mini is the sandbox that makes it real.

| Track | Phase | Status |
|-------|-------|--------|
| AI | Phase 1 — Agent Foundation | ✅ COMPLETE (Hermes + GPT-5.5 on Mac Mini, Telegram connected) |
| Infra | Phase 2 — Home Lab Substrate | ✅ COMPLETE (SSH ✅ static IP ✅ Homebrew ✅ Tailscale ✅ Screen Sharing ✅ Ollama/qwen3.5:9b ✅ Docker ✅ HAOS 17.3 ✅ Hermes+Telegram ✅) |
| AI | Phase 3 — Connected Agents + MCP | ▶️ ACTIVE (HA MCP read access working; writes approval-gated) |
| Infra | Phase 4 — Local Intelligence | 📋 Planned |
| AI | Phase 5 — Multi-Agent & Autonomous | 📋 Planned |
| Infra | Phase 6 — GPU Stack | ⏸ Conditional (camera migration only) |
| AI | Phase 7 — Mastery + Sovereignty | 📋 Planned |
