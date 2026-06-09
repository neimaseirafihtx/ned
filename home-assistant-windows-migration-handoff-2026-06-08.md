# Home Assistant Windows Migration Handoff

Created: 2026-06-08 20:35 CDT
Owner: Neima / Ned
Purpose: move Home Assistant from the Mac mini/UTM setup to the PowerSpec Windows 11 Pro PC, and preserve every known file/config path linked to rebuilding HA, HAOS, Hermes MCP, dashboards, scenes, scripts, and monitoring.

## Direct recommendation

Use HAOS in a VM on the Windows PC, not Home Assistant Container as the primary migration target.

Reason: this setup already depends on the full Home Assistant experience: add-ons, official MCP Server integration, clean backup/restore, dashboards, scripts, scenes, and future expansion. HA Container in Docker is useful for experiments, but it is a second-class target for Neima's primary smart-home brain.

Best target on Windows:

1. Hyper-V VM running HAOS x86_64, if Hyper-V is enabled and acceptable.
2. VMware/VirtualBox HAOS VM, if Hyper-V/Docker Desktop conflicts become annoying.
3. Docker Home Assistant Container only as a fallback/test build, not the long-term primary.

## Current live status observed from Mac mini

As of 2026-06-08 20:35 CDT:

- `192.168.68.68` responds to ping.
- `http://192.168.68.68:8123/api/` returned connection refused.
- `http://homeassistant.local:8123/api/` did not resolve from the Mac mini session.
- ARP still shows `192.168.68.68` on Mac mini wired interface `en9` with MAC `2e:48:ea:d5:95:a4`.
- `utmctl list` is not usable from this session; it returns macOS automation error `OSStatus error -1743`, which is known/expected from SSH/non-GUI contexts.
- Current UTM app container path only showed `/Users/neimaseirafi/Library/Containers/com.utmapp.UTM/Data`; the active VM bundle was not visible there during this check.
- The HAOS VM artifacts are present in the Mac mini migration backup under `~/mac-mini-migration-backups/...`.

Interpretation: HA is not currently reachable over port 8123 from this Mac mini session, but the HA IP still answers ping. Before migration, try to boot/recover HA once and create a fresh Home Assistant full backup from the HA UI. If that cannot be done, use the copied HAOS qcow2/UTM VM disk backup as the recovery source.

## Primary source artifacts to preserve/copy

### 1. HAOS VM disk and UTM config from Mac mini migration backup

These are the most important recovery artifacts if a normal HA backup cannot be created.

Primary backup copy:

```text
/Users/neimaseirafi/mac-mini-migration-backups/mac-mini-config-backup-20260606T233300Z/utm/Linux.utm
/Users/neimaseirafi/mac-mini-migration-backups/mac-mini-config-backup-20260606T233300Z/utm/Linux.utm/Linux.utm
/Users/neimaseirafi/mac-mini-migration-backups/mac-mini-config-backup-20260606T233300Z/utm/Linux.utm/Linux.utm/config.plist
/Users/neimaseirafi/mac-mini-migration-backups/mac-mini-config-backup-20260606T233300Z/utm/Linux.utm/Linux.utm/Data/efi_vars.fd
/Users/neimaseirafi/mac-mini-migration-backups/mac-mini-config-backup-20260606T233300Z/utm/Linux.utm/Linux.utm/Data/haos.qcow2
```

Robust supplement duplicate:

```text
/Users/neimaseirafi/mac-mini-migration-backups/mac-mini-config-backup-20260606T233300Z/robust-supplement-20260607T011639Z/utm/com.utmapp.UTM/com.utmapp.UTM/Data/Documents/Linux.utm
/Users/neimaseirafi/mac-mini-migration-backups/mac-mini-config-backup-20260606T233300Z/robust-supplement-20260607T011639Z/utm/com.utmapp.UTM/com.utmapp.UTM/Data/Documents/Linux.utm/Data/haos.qcow2
```

Verified artifact size:

```text
haos.qcow2: 7,005,732,864 bytes
modified: 2026-06-02 09:11:42 CDT
```

UTM config facts extracted from `config.plist`:

```yaml
name: Linux
uuid: 56E37577-9321-4F8C-A5AA-918F7B382841
backend: QEMU
architecture: aarch64
cpu_count: 2
memory_mb: 2048
disk_image: Data/haos.qcow2
disk_interface: VirtIO
network_mode: Bridged
bridge_interface_on_mac: en9
vm_mac_address: 86:4A:B6:55:3B:AE
uefi_boot: true
```

Important: this is an ARM64/aarch64 HAOS VM disk from Apple Silicon. It probably will not boot directly as a Windows x86_64 VM. Treat it as a recovery artifact, not the preferred final runtime. The preferred Windows migration path is still: create a fresh HAOS x86_64 VM, restore a Home Assistant full backup.

### 2. Home Assistant normal full backup

This is the best migration artifact, but it was not found in the Mac mini backup inventory and HA was not reachable during this check.

Before final cutover, try to create one from HA:

```text
Settings -> System -> Backups -> Create backup
Backup type: full backup
Download the .tar backup file
Store it under the Windows restore staging folder, e.g. C:\restore\home-assistant\backups\
```

If HA UI cannot be reached, attempt to recover/boot the existing VM first, then create the backup. If still impossible, recover from the qcow2 disk backup.

### 3. Ned repo Home Assistant documentation and rebuild sources

Canonical repo:

```text
/Users/neimaseirafi/Documents/ned
```

Files directly linked to HA rebuild/migration:

```text
/Users/neimaseirafi/Documents/ned/references/homelab-stack.md
/Users/neimaseirafi/Documents/ned/plans/home-assistant-mcp-roadmap.md
/Users/neimaseirafi/Documents/ned/plans/home-assistant-usability-pass.md
/Users/neimaseirafi/Documents/ned/references/home-assistant-entity-map.md
/Users/neimaseirafi/Documents/ned/references/home-assistant-automation-inventory.md
/Users/neimaseirafi/Documents/ned/references/home-assistant-script-drafts.yaml
/Users/neimaseirafi/Documents/ned/references/assets/network-topology/deco-clients-personal-homeassistant.jpg
/Users/neimaseirafi/Documents/ned/scripts/mac-mini-health-check.sh
/Users/neimaseirafi/Documents/ned/roadmap/roadmap.yaml
/Users/neimaseirafi/Documents/ned/roadmap/index.html
```

Role of each file:

- `references/homelab-stack.md`: strategic HA recommendation; says HAOS VM is preferred over Docker Container because add-ons/supervised/backup restore matter.
- `plans/home-assistant-mcp-roadmap.md`: MCP architecture, safe-control boundaries, official MCP Server endpoint, token/Hermes connection plan, write-safety rules.
- `plans/home-assistant-usability-pass.md`: dashboard plan, created `Neima Home` dashboard details, first useful rooms, exact scene/script targets.
- `references/home-assistant-entity-map.md`: curated entity map from live HA API/MCP; use it to verify entity IDs after restore.
- `references/home-assistant-automation-inventory.md`: Apple Home / Google Home / Hue / Lutron source automation inventory and migration decisions.
- `references/home-assistant-script-drafts.yaml`: exact YAML drafts for `scene.family_room_evening`, `scene.family_room_movie`, `script.family_room_evening`, `script.family_room_movie`.
- `references/assets/network-topology/deco-clients-personal-homeassistant.jpg`: Deco client screenshot/reference for Home Assistant network identity.
- `scripts/mac-mini-health-check.sh`: old Mac mini health check that includes HA reachability checks; after migration, rewrite for Windows/new host.
- `roadmap/roadmap.yaml`: canonical roadmap includes HA MCP/read access, safe light control, dashboard, automation migration, and boot reliability items.
- `roadmap/index.html`: generated roadmap viewer.

Current repo state when this handoff was created:

```text
/Users/neimaseirafi/Documents/ned is on main tracking origin/main.
Uncommitted/untracked items existed:
  M memory/.DS_Store
  ?? plans/ray-ai-power-session-agenda-updated-final-objectives.html
  ?? ray-migration-handoff-2026-06-08.md
  ?? home-assistant-windows-migration-handoff-2026-06-08.md
```

### 4. Hermes MCP config and token references

Default Hermes profile config:

```text
/Users/neimaseirafi/.hermes/config.yaml
/Users/neimaseirafi/.hermes/.env
```

HA-local Hermes profile config:

```text
/Users/neimaseirafi/.hermes/profiles/ha-local/config.yaml
/Users/neimaseirafi/.hermes/profiles/ha-local/.env
```

Default profile MCP server config, redacted:

```yaml
mcp_servers:
  homeassistant:
    url: http://homeassistant.local:8123/api/mcp
    headers:
      Authorization: Bearer ${HA_MCP_TOKEN}
    timeout: 120
    connect_timeout: 60
```

HA-local profile MCP server config, redacted:

```yaml
mcp_servers:
  homeassistant:
    url: http://homeassistant.local:8123/api/mcp
    headers:
      Authorization: Bearer ${HA_MCP_TOKEN}
    timeout: 120
    connect_timeout: 60
    enabled: false
```

Relevant `.env` variable names, values intentionally not copied here:

```text
HA_MCP_URL
HA_MCP_TOKEN
HA_MCP_TIMEZONE
```

Security note: do not paste the actual long-lived access token into docs or Git. On the Windows Hermes instance, either migrate the token securely or create a new dedicated Home Assistant long-lived token after HA is restored, then update Windows Hermes `.env`.

### 5. Hermes skills and reference files tied to HA/MCP

Skills used for this environment:

```text
~/.hermes/skills/smart-home/home-assistant-mcp-operations/SKILL.md
~/.hermes/skills/smart-home/home-assistant-mcp-operations/references/home-assistant-mcp-direct-verification.md
~/.hermes/skills/smart-home/home-assistant-mcp-operations/references/home-assistant-mcp-local-profile-notes.md
~/.hermes/skills/smart-home/home-assistant-mcp-operations/references/home-assistant-mcp-safe-surface.md
~/.hermes/skills/mcp/native-mcp/SKILL.md
~/.hermes/skills/mcp/native-mcp/references/home-assistant-official-mcp.md
~/.hermes/skills/mcp/native-mcp/references/home-assistant-mcp-hermes.md
~/.hermes/skills/mcp/native-mcp/references/home-assistant-token-auth-pitfalls.md
~/.hermes/skills/mcp/native-mcp/references/home-assistant-live-context-curated-map.md
~/.hermes/skills/mcp/native-mcp/references/home-assistant-safe-mcp-surface.md
~/.hermes/skills/smart-home/home-assistant-usability-migration/SKILL.md
```

If Windows Hermes does not yet have these skills, install/copy them or rely on the Ned repo docs above. The Ned repo files are the more important durable project source.

## Home Assistant content known to exist / be expected after restore

### Core URL and network identity

Current expected HA URLs:

```text
http://homeassistant.local:8123
http://192.168.68.68:8123
MCP endpoint: http://homeassistant.local:8123/api/mcp
```

After migration, decide whether to preserve `192.168.68.68` for Home Assistant on the Windows host/VM or assign a new reservation. If the IP changes, update:

- Windows Hermes `.env` / config if it uses a fixed URL.
- `~/.hermes/config.yaml` equivalent on Windows.
- health checks / cron scripts.
- Deco reservation notes.
- any bookmarks/mobile app server URL.

Recommended: reserve a stable IP for the new HA VM/container in Deco. If possible, keep `192.168.68.68` to reduce breakage.

### Integrations already part of the HA setup

Known integrations/devices represented in docs/entity map:

- Philips Hue
- Lutron Caseta
- Sonos
- Samsung TV / display entities
- TP-Link Deco / BE63 network sensors
- weather/home forecast entity
- Neima person entity, not yet useful as a tracker
- official Home Assistant MCP Server integration

Deferred/not primary:

- Nest thermostat/cameras: deferred.
- Frigate/NVR/local cameras: deferred.
- HVAC/cameras/security controls: off-limits for casual agent control.

### Dashboard

Known dashboard:

```text
Title: Neima Home
URL path: /neima-home/home
Sidebar: shown
Old rollback path: /ned-home/home hidden from sidebar
```

Known first button grid:

```text
Second Floor Scenes
script.family_room_evening
script.family_room_movie
script.all_house_lights_off
```

Known room cards:

```text
Family Room
Kitchen / Dining
Entryway
Neima's Room
Listening Room
Guestroom
Office / Garage
Exterior
```

After restore, verify the dashboard exists and the script buttons still call `script.turn_on` directly.

### Scenes/scripts expected

Known HA-created scenes/scripts:

```text
scene.family_room_evening
scene.family_room_movie
script.family_room_evening
script.family_room_movie
script.all_house_lights_off
```

Known supporting script drafts:

```text
/Users/neimaseirafi/Documents/ned/references/home-assistant-script-drafts.yaml
```

Critical implementation pitfall:

Home Assistant scene config needs flattened attributes:

```yaml
light.example:
  state: "on"
  brightness: 128
```

Do not use REST-state-shaped nested attributes like:

```yaml
light.example:
  state: "on"
  attributes:
    brightness: 128
```

For the dashboard, scripts worked more reliably than scenes. The Family Room area page's auto scene trigger did not drive physical lights, while Developer Tools `script.turn_on` worked. Prefer `script.family_room_*` buttons.

### Exact migrated scene targets

Evening:

```text
light.kitchen_island_pendants: on, 30%
light.kitchen_main_lights: off
light.tv_lightstrip: on, 28%
light.family_room_lamp: on, 75%
light.family_room_main_lights: on, 1%
light.dining_room_main_lights: on, 20%
```

Movie:

```text
light.kitchen_island_pendants: on, 35%
light.tv_lightstrip: on, 19%
light.family_room_lamp: on, 25%
light.family_room_main_lights: off
light.dining_room_main_lights: off
```

Family Room Off must include all four, not just the Hue group:

```text
light.family_room
light.family_room_lamp
light.tv_lightstrip
light.family_room_main_lights
```

### Automation/source-app inventory

Keep source apps in place until HA replacements are proven.

Known source automations/scenes:

- Apple Home `Evening`: migrated/translated to HA script/scene.
- Apple Home `Movie`: migrated/translated to HA script/scene.
- Google Home `All Lights Off` at 11 PM: replace later with exact HA script/automation, not broad targeting.
- Hue `Morning Lamp` 7-9 AM: defer/maybe leave.
- Hue `Evening Lamps` 5-11 PM: leave for now; maybe replace later.
- Lutron `Outdoor Lights` sunset: leave in Lutron.
- Lutron `Outdoor Lights Off` 11:30 PM: leave in Lutron.
- Lutron `Smart Bridge 2 All Second Floor`: broad scope; review carefully, do not expose casually.

## MCP safety policy to preserve

Allowed routine reads:

- `GetLiveContext`
- `GetDateTime`
- read-only todo queries if useful
- broad state reads, interpreted through `references/home-assistant-entity-map.md`

Allowed routine writes, only after explicit scope is stable:

- exact `light.*` entities
- exact light groups
- brightness/color/on/off for approved lights
- exact approved scripts such as `script.family_room_evening`, `script.family_room_movie`, `script.all_house_lights_off`

Off-limits by default:

- Sonos/media-player control
- TVs/display media players
- locks/garage/security
- cameras
- HVAC/thermostat
- broad automation/config edits
- arbitrary `call_service` style control
- ambiguous room-wide control that could hit unintended devices

Important MCP pitfall:

The official MCP Server's `HassLightSet` uses natural-language selectors rather than strict entity IDs. In a prior test, setting Family Room Main Lights with both `name` and `area` also nudged other Family Room lights. For routine control, prefer exact HA scripts or an allowlisted wrapper over broad natural-language Assist targeting.

## Windows migration plan

### Phase 0: decide runtime target

Recommended:

```text
Windows 11 Pro -> Hyper-V -> HAOS x86_64 VM
```

Avoid making Docker Container the primary unless we intentionally accept losing add-ons/supervised features. Docker is fine for temporary HA test restore only if needed.

### Phase 1: create/collect the best backup

Preferred:

1. Bring old HA up on Mac if possible.
2. In HA UI, create a full backup.
3. Download the backup `.tar`.
4. Copy it to Windows staging:

```text
C:\restore\home-assistant\backups\
```

Fallback if HA UI cannot be reached:

1. Copy `haos.qcow2` from the Mac migration backup.
2. Attempt to mount/convert/extract the HA data partition or boot it in an ARM-capable recovery environment.
3. If extraction is not practical, preserve the qcow2 as a rollback artifact and rebuild HA fresh using the Ned docs/entity map/scripts.

### Phase 2: build fresh HAOS on Windows

For Hyper-V:

1. Download current HAOS x86_64 image from Home Assistant's official Windows/Generic x86-64 instructions.
2. Create VM with roughly:
   - 2 vCPU minimum, 4 vCPU is fine on the PowerSpec.
   - 4 GB RAM minimum; 6-8 GB is fine if available.
   - 32+ GB disk.
   - bridged/external virtual switch so HA is visible on LAN and mDNS works.
3. Boot HAOS.
4. Reserve a stable IP in Deco, ideally `192.168.68.68` if no conflict.
5. Restore the full HA backup during onboarding.
6. Verify `http://homeassistant.local:8123` and the fixed IP.

### Phase 3: restore Home Assistant and verify integrations

After restore:

- Confirm Hue integration works.
- Confirm Lutron Caseta works.
- Confirm Sonos is visible.
- Confirm dashboard `/neima-home/home` exists.
- Confirm scripts exist and can run from Developer Tools.
- Confirm official MCP Server integration is installed.
- Confirm exposed entities/control setting matches policy.
- Confirm mobile Companion App uses new server/IP.

### Phase 4: reconnect Windows Hermes MCP

On the Windows Hermes instance:

1. Add/create a dedicated HA long-lived token.
2. Put it in Windows Hermes `.env`, do not commit it.
3. Configure MCP server:

```yaml
mcp_servers:
  homeassistant:
    url: http://homeassistant.local:8123/api/mcp
    headers:
      Authorization: Bearer ${HA_MCP_TOKEN}
    timeout: 120
    connect_timeout: 60
```

If mDNS is flaky on Windows, use the fixed IP temporarily:

```yaml
url: http://192.168.68.68:8123/api/mcp
```

4. Restart Hermes.
5. Run `hermes mcp list`.
6. Verify `homeassistant` is enabled and tools are discovered.
7. In a fresh session, do a read-only live context test first.
8. Do not run light writes until reads are verified against the entity map.

### Phase 5: move health checks/cron

Old Mac script:

```text
/Users/neimaseirafi/Documents/ned/scripts/mac-mini-health-check.sh
```

After HA moves to Windows:

- Replace Mac-specific checks with Windows host checks.
- Keep HA URL checks.
- Decide whether Mac mini health reports should be retired or become Windows server health reports.
- Cron reports should deliver to main Telegram DM only.

## Docker Container fallback notes

Only use this if VM setup is blocked or for a quick test.

Example shape:

```yaml
services:
  homeassistant:
    container_name: homeassistant
    image: ghcr.io/home-assistant/home-assistant:stable
    volumes:
      - C:/homeassistant/config:/config
    environment:
      - TZ=America/Chicago
    network_mode: host  # not normally available the same way on Docker Desktop for Windows
    restart: unless-stopped
```

Gotchas:

- Docker Desktop on Windows does not give Linux containers true LAN host networking in the same clean way as Linux.
- mDNS/discovery for Hue/Sonos/Lutron may be worse.
- No HA add-on store/supervisor.
- Backup/restore story is less friendly.

So: do not make this the primary unless we intentionally choose a reduced HA footprint.

## Cutover checklist

Before cutover:

- [ ] Fresh HA full backup downloaded if HA UI can be recovered.
- [ ] Existing `haos.qcow2` copied to Windows staging as rollback artifact.
- [ ] Ned repo copied/pulled on Windows.
- [ ] Windows HAOS VM created and bridged to LAN.
- [ ] Stable IP reservation set in Deco.
- [ ] HA restored and reachable at browser URL.
- [ ] Hue/Lutron/Sonos verified.
- [ ] `Neima Home` dashboard verified.
- [ ] Family Room Evening/Movie scripts verified manually.
- [ ] Official MCP Server integration verified.
- [ ] Dedicated HA token created for Hermes.
- [ ] Windows Hermes `.env` updated with `HA_MCP_TOKEN`.
- [ ] Windows Hermes `mcp_servers.homeassistant` configured.
- [ ] `hermes mcp list` shows `homeassistant` enabled.
- [ ] First MCP read-only live context verified.
- [ ] Entity map spot-check passes.
- [ ] Mac Hermes cron/health reports either migrated or retired.
- [ ] Old Mac HA VM kept powered off but not deleted until Windows HA is stable for several days.

## Verification commands / tests

From Windows PowerShell after HA comes up:

```powershell
Test-NetConnection 192.168.68.68 -Port 8123
Invoke-WebRequest http://192.168.68.68:8123/api/ -UseBasicParsing
```

Expected unauthenticated API behavior can be `401`/auth-gated or a small API message depending endpoint/version. Connection refused is not OK.

From Windows Hermes terminal:

```bash
hermes mcp list
hermes profile list
hermes status --all
```

Read-only MCP test in Hermes:

```text
Using Home Assistant MCP, read live context only and summarize which lights are on. Do not control anything.
```

Then compare against:

```text
/Users/neimaseirafi/Documents/ned/references/home-assistant-entity-map.md
```

or the Windows-cloned equivalent path.

## Things not to lose

- HA full backup if available.
- `haos.qcow2` rollback artifact.
- Dashboard `/neima-home/home`.
- `script.family_room_evening` and `script.family_room_movie`.
- `script.all_house_lights_off` if present.
- Official MCP Server integration.
- Dedicated HA long-lived access token or ability to create a new one.
- Deco DHCP reservation / stable HA IP.
- Entity map and automation inventory in Ned repo.
- Safety boundary: lights okay; Sonos/TV/HVAC/security/cameras not casual-write targets.

## Open questions for final migration session

1. Can the old HA UI be brought up long enough to create a full backup?
2. Should the Windows HA VM keep `192.168.68.68`, or should Deco assign a new reservation?
3. Which virtualization layer on the PowerSpec is preferred: Hyper-V, VMware, or VirtualBox?
4. Is Docker Desktop already needed for Ray/Hermes on Windows, and will it conflict with Hyper-V choices?
5. Should Windows Hermes become the sole owner of HA MCP and HA-related cron reports?
6. How long should the Mac mini HA VM rollback artifact be retained after cutover?
