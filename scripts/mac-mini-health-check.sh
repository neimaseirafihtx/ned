#!/usr/bin/env bash
set -u

# Mac mini homelab health check.
# Designed for both manual runs and Hermes cron no_agent delivery.
# Prints a concise status brief. Exit 0 so Hermes cron delivers the report even
# when a monitored service is failing; the message body carries FAIL/WARN state.

HOST="Neimas-Mac-mini.local"
CANONICAL_IP="192.168.68.85"
CANONICAL_IFACE="en9"
CANONICAL_MAC="6c:1f:f7:c0:3e:e5"
HA_IP="192.168.68.68"
HA_URL_IP="http://${HA_IP}:8123/"
HA_URL_LOCAL="http://homeassistant.local:8123/"

fails=()
warns=()
oks=()

ok() { oks+=("$1"); }
warn() { warns+=("$1"); }
fail() { fails+=("$1"); }

have() { command -v "$1" >/dev/null 2>&1; }

http_code() {
  local url="$1"
  curl -fsS --max-time 5 -o /dev/null -w '%{http_code}' "$url" 2>/dev/null || true
}

# Host / network identity
hostname_now="$(hostname 2>/dev/null || true)"
if [[ "$hostname_now" == "$HOST" ]]; then
  ok "Hostname: ${hostname_now}"
else
  warn "Hostname expected ${HOST}, got ${hostname_now:-unknown}"
fi

ip_now="$(ipconfig getifaddr "$CANONICAL_IFACE" 2>/dev/null || true)"
if [[ "$ip_now" == "$CANONICAL_IP" ]]; then
  ok "LAN: ${CANONICAL_IFACE} has ${CANONICAL_IP}"
else
  fail "LAN: ${CANONICAL_IFACE} expected ${CANONICAL_IP}, got ${ip_now:-none}"
fi

iface_info="$(ifconfig "$CANONICAL_IFACE" 2>/dev/null || true)"
if grep -q "ether ${CANONICAL_MAC}" <<<"$iface_info"; then
  ok "Adapter MAC: ${CANONICAL_MAC}"
else
  fail "Adapter MAC mismatch or ${CANONICAL_IFACE} missing"
fi
if grep -q "2500Base-T" <<<"$iface_info" && grep -q "status: active" <<<"$iface_info"; then
  ok "Adapter link: 2500Base-T active"
else
  fail "Adapter link: expected 2500Base-T active"
fi

# Hermes gateway
if have hermes; then
  gateway_status="$(hermes gateway status 2>&1 || true)"
  if grep -q "Gateway service is loaded" <<<"$gateway_status" && grep -q '"PID"' <<<"$gateway_status"; then
    ok "Hermes gateway: loaded/running"
  else
    fail "Hermes gateway: not clearly running"
  fi
else
  fail "Hermes CLI not found"
fi

# Tailscale
if have tailscale; then
  ts_status="$(tailscale status --peers=false 2>&1 || true)"
  if grep -q "neimas-mac-mini" <<<"$ts_status"; then
    ok "Tailscale: connected"
  else
    fail "Tailscale: not connected or unexpected status"
  fi
else
  fail "Tailscale CLI not found"
fi

# Ollama
ollama_code="$(http_code 'http://127.0.0.1:11434/api/tags')"
if [[ "$ollama_code" == "200" ]]; then
  ok "Ollama: API reachable"
else
  fail "Ollama: API not reachable"
fi

# Docker
if have docker; then
  docker_info="$(docker info --format '{{.ServerVersion}}' 2>&1 || true)"
  if [[ "$docker_info" =~ ^[0-9] ]]; then
    ok "Docker: running (${docker_info})"
  else
    warn "Docker: not reachable (${docker_info//$'\n'/ })"
  fi
else
  warn "Docker CLI not found"
fi

# UTM / Home Assistant VM. utmctl may not work over SSH, so HA HTTP is the source of truth.
if have utmctl; then
  utm_out="$(utmctl list 2>&1 || true)"
  if grep -q "Linux" <<<"$utm_out"; then
    ok "UTM: Linux VM visible to utmctl"
  elif grep -q "does not work from SSH" <<<"$utm_out" || grep -q "OSStatus error -1743" <<<"$utm_out"; then
    warn "UTM: utmctl not queryable from SSH; using HA HTTP as VM proof"
  else
    warn "UTM: Linux VM not visible in utmctl output"
  fi
else
  warn "UTM: utmctl not found"
fi

ha_code_ip="$(http_code "$HA_URL_IP")"
ha_code_local="$(http_code "$HA_URL_LOCAL")"
if [[ "$ha_code_ip" == "200" || "$ha_code_ip" == "401" || "$ha_code_ip" == "302" ]]; then
  ok "Home Assistant: ${HA_IP}:8123 reachable (${ha_code_ip})"
else
  fail "Home Assistant: ${HA_IP}:8123 not reachable (${ha_code_ip:-no response})"
fi
if [[ "$ha_code_local" == "200" || "$ha_code_local" == "401" || "$ha_code_local" == "302" ]]; then
  ok "Home Assistant mDNS: homeassistant.local reachable (${ha_code_local})"
else
  warn "Home Assistant mDNS: homeassistant.local not reachable (${ha_code_local:-no response})"
fi

# SMB
if nc -vz -w 3 127.0.0.1 445 >/dev/null 2>&1; then
  ok "SMB: local port 445 open"
else
  fail "SMB: local port 445 not open"
fi

# Storage
root_line="$(df -h / 2>/dev/null | tail -1)"
root_free="$(awk '{print $4}' <<<"$root_line" 2>/dev/null || true)"
root_used_pct="$(awk '{print $5}' <<<"$root_line" 2>/dev/null || true)"
if [[ -n "$root_free" ]]; then
  ok "Root disk: ${root_free} free (${root_used_pct} used)"
else
  warn "Root disk: df failed"
fi

external_found=0
for vol in "/Volumes/MacStorage" "/Volumes/Mac External" "/Volumes/T9Storage" "/Volumes/DataDrive"; do
  if [[ -d "$vol" ]]; then
    external_found=1
    line="$(df -h "$vol" 2>/dev/null | tail -1)"
    free="$(awk '{print $4}' <<<"$line" 2>/dev/null || true)"
    used="$(awk '{print $5}' <<<"$line" 2>/dev/null || true)"
    ok "External storage: ${vol} mounted, ${free:-unknown} free (${used:-?} used)"
  fi
done
if [[ "$external_found" == "0" ]]; then
  warn "External storage: no known T9/Mac storage volume mounted"
fi

# Output
now="$(date '+%Y-%m-%d %H:%M:%S %Z')"
if (( ${#fails[@]} == 0 && ${#warns[@]} == 0 )); then
  echo "Mac mini health: all green — ${now}"
  printf '✓ %s\n' "${oks[@]}"
elif (( ${#fails[@]} == 0 )); then
  echo "Mac mini health: green with warnings — ${now}"
  printf '✓ %s\n' "${oks[@]}"
  printf '⚠ %s\n' "${warns[@]}"
else
  echo "Mac mini health: FAIL — ${now}"
  printf '✗ %s\n' "${fails[@]}"
  printf '⚠ %s\n' "${warns[@]}"
  printf '✓ %s\n' "${oks[@]}"
fi

# Cron delivery should succeed even when the health report says FAIL.
# A non-zero exit makes Hermes treat the job itself as broken, which can hide
# the useful stdout behind an error path.
exit 0
