# Home Lab Stack — HA, Frigate, Docker, Networking

Last updated: 2026-06-09

> **Platform note (2026-06-09):** the Mac Mini was decommissioned and returned. The home lab server is now the Windows PowerSpec PC (`192.168.68.89`). Mac-specific instructions below (UTM, Homebrew, macOS Docker caveats) are kept for historical context only. HA is currently offline pending restore on Windows — see `home-assistant-windows-migration-handoff-2026-06-08.md`.

## Home Assistant

### How to install on the Windows server

**Use HAOS in a VM — not Docker Container.** This is important.

Docker Container (HADC) works but is a second-class citizen. It loses:
- Add-ons (Mosquitto, ESPHome, Node-RED, etc. all live in HA's add-on system)
- Supervised mode features
- Simpler backup/restore

**Best option on Windows:** Hyper-V VM running HAOS x86_64 (VMware/VirtualBox if Hyper-V conflicts get annoying; Docker Container only as a throwaway test build).
1. Download the HAOS x86_64 `.vhdx` image from https://www.home-assistant.io/installation/ (Windows/Generic x86-64 instructions)
2. Create a Hyper-V Gen 2 VM with an **external switch** bridged to the LAN so HA gets its own LAN IP (mDNS/discovery for Hue, Sonos, Caseta need this), disable Secure Boot, attach the vhdx
3. Allocate 2 vCPU, 2-4GB RAM — HAOS is lightweight
4. HA runs at `http://homeassistant.local:8123` → restore the full backup from `C:\restore\home-assistant\backups\`

This gives you the full HA experience including add-ons. The old ARM64 `haos.qcow2` from the Mac is a recovery artifact only — it won't boot as an x86_64 VM.

<details>
<summary>Historical: install on Mac Mini (decommissioned)</summary>

**Best option for Mac Mini:** UTM (free) or Parallels, running HAOS as a VM.
1. Download HAOS `.qcow2` image from https://www.home-assistant.io/installation/
2. Create UTM VM, attach the image, boot
3. Allocate 2 CPU cores, 2-4GB RAM to the VM — HAOS is lightweight
4. HA runs at `http://homeassistant.local:8123`

</details>

### Integrations in order of difficulty

**Easy (auto-discovered or near-instant):**
1. **Philips Hue** — discovers via mDNS, click approve on the bridge
2. **Sonos** — auto-discovers on the same network, plug-and-play
3. **Lutron Caseta** — requires the Caseta Smart Bridge (not the Pro), local API via PySSDP

**Medium:**
4. **Lutron Caseta Pro Bridge** — if you have the Pro model, use the local Telnet integration

**Annoying:**
5. **Nest thermostat** — requires Google account OAuth, Google Device Access Program enrollment ($5 one-time fee, ~5 min approval), and creating a GCP project. The integration works great once set up but the setup is a maze. Budget 30-45 minutes. Instructions: https://www.home-assistant.io/integrations/nest/

### Useful add-ons (HAOS only)
- **Mosquitto MQTT broker** — needed for many DIY sensors
- **Node-RED** — visual automation flows, easier than YAML for complex logic
- **ESPHome** — if you ever add DIY sensors/switches
- **File Editor** — edit config files from the UI

---

## Frigate NVR

### What Frigate does
AI-powered NVR. It records video AND runs object detection (people, cars, animals) on the stream. Much smarter than a dumb NVR.

### Running on Mac Mini (important caveats)

**The problem:** Frigate needs hardware acceleration for object detection. On Linux it can use GPU directly. On macOS + Docker, hardware passthrough is limited.

**Your options:**

1. **Software-only detection (no Coral)** — works out of the box, but CPU-intensive. Mac Mini M4 can handle ~2-4 cameras at 5fps detection. Not ideal but functional.

2. **Coral USB TPU** — the right answer for serious use. BUT: USB passthrough to Docker on macOS is unreliable. The Coral USB Accelerator often doesn't pass through cleanly to Docker containers on macOS.

   Workaround: Run Frigate in a Linux VM (UTM) on the Mac Mini instead of bare Docker. USB passthrough to a UTM VM works. This is the cleaner path if you want Coral.

3. **Run Frigate on Linux** — if you eventually have a Linux machine, Coral USB works perfectly there.

**For Neima's current setup:** Start with software-only detection in Docker. It'll work. Add Coral later once you decide if Frigate is worth investing in further.

### Reolink 810A RTSP URLs

```
# Main stream (2K/4K — high res, high bandwidth)
rtsp://<username>:<password>@<camera-ip>:554/h264Preview_01_main

# Sub stream (lower res — use this for Frigate detection)
rtsp://<username>:<password>@<camera-ip>:554/h264Preview_01_sub
```

**Use the sub stream for Frigate's detect role.** The main stream is for recording. This halves the CPU load on object detection without losing recording quality.

Default Reolink creds: `admin` / (blank password on first setup, then you set one)

**Test your RTSP URL with VLC first:**
```
# In VLC: Media → Open Network Stream → paste URL
# Or command line:
ffplay "rtsp://admin:yourpassword@192.168.1.100:554/h264Preview_01_sub"
```

If VLC can't connect, Frigate won't either. Fix auth/network first.

**URL encoding:** If your password has special characters (@, #, etc.), URL-encode them. `@` becomes `%40`.

### NVR + Frigate dual-stream (your setup)

**Yes, the Reolink NVR and Frigate can both pull from the same camera simultaneously.** Reolink 810A supports multiple concurrent RTSP streams.

- NVR pulls main stream for recording
- Frigate pulls sub stream for detection
- No conflict, no degradation

If you see dropped frames or stream errors: check your router/switch. The camera is pushing two streams, which adds bandwidth. Most home routers handle this fine but cheap unmanaged switches can be flaky.

### Frigate config snippet (Docker)

```yaml
# docker-compose.yml
services:
  frigate:
    image: ghcr.io/blakeblackshear/frigate:stable
    restart: unless-stopped
    volumes:
      - ./config:/config
      - /path/to/storage:/media/frigate
    ports:
      - "5000:5000"
      - "8971:8971"
    environment:
      FRIGATE_RTSP_PASSWORD: "yourpassword"
```

```yaml
# config/config.yml
mqtt:
  enabled: false  # set to true if you have Mosquitto running

cameras:
  front_door:
    ffmpeg:
      inputs:
        - path: rtsp://admin:{FRIGATE_RTSP_PASSWORD}@192.168.1.100:554/h264Preview_01_main
          roles:
            - record
        - path: rtsp://admin:{FRIGATE_RTSP_PASSWORD}@192.168.1.100:554/h264Preview_01_sub
          roles:
            - detect
    detect:
      width: 640
      height: 360
      fps: 5
    record:
      enabled: true
      retain:
        days: 7
```

---

## Docker on Mac Mini

Docker Desktop is fine for the Mac Mini server use case. A few notes:

- Resources: give Docker at least 4 CPU cores and 4GB RAM in Docker Desktop settings
- Volumes: use named volumes for persistent data (databases, configs, media)
- `host.docker.internal` resolves to the Mac's IP from inside containers — use this when a container needs to reach another service on the host

### Useful containers to run

| Container | Purpose | Port |
|-----------|---------|------|
| `ghcr.io/open-webui/open-webui` | Ollama chat UI | 3000 |
| `ghcr.io/blakeblackshear/frigate:stable` | NVR + AI detection | 5000, 8971 |
| `portainer/portainer-ce` | Docker management UI | 9000 |
| `linuxserver/heimdall` | Dashboard/home page | 80 |

---

## Tailscale (Remote Access)

Dead simple. Install on every device you want to reach:

```bash
brew install --cask tailscale
```

Or use Docker:
```bash
docker run -d \
  --name=tailscale \
  --network=host \
  --cap-add=NET_ADMIN \
  --cap-add=SYS_MODULE \
  -v /var/lib/tailscale:/var/lib/tailscale \
  tailscale/tailscale tailscaled
```

Each device gets a `100.x.x.x` IP and a `<device>.tail<hash>.ts.net` hostname. Works through NAT, no port forwarding needed.

**For HA remote access:** Nabu Casa (HA Cloud, $7/mo) is easier than self-hosting remote access. But Tailscale + direct HA access is free and fast if you don't mind the setup.

---

## Networking Tips

- Put your cameras on a dedicated VLAN or at least a guest network. Reolink cameras phone home more than you'd like.
- Static IPs for the Mac Mini, cameras, and anything Frigate/HA talks to. Set these in your router DHCP reservations, not on the devices themselves.
- mDNS (`.local` hostnames) works great on the local network but doesn't traverse VLANs without mDNS repeater/Avahi.
