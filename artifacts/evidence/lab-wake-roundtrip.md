# Evidence: cold Wake-on-LAN round trip + box dial-in (2026-06-12)

## Cold WoL round trip (the full operator loop)

```
$ ssh substrate-lab 'sudo systemctl poweroff'     # box fully off (ssh dead)
$ labctl lab wake --wait --timeout 180
magic packet sent (broadcast 255.255.255.255:9)
waiting for ssh on substrate-lab (timeout 180s)...
lab host is reachable
exit=0
```

Post-boot verification, all in one probe:

```
LID: HandleLidSwitch=ignore
SUSPEND: masked
WLAN: Device "wlp4s0" does not exist.   <- iwlwifi blacklisted, wifi gone
UFW: Status: active
DOCKER: active group-ok
TAILSCALE: 100.88.24.45
CLAUDE: "loggedIn": true
GH: ok
REPO: 0097c33-2026-06-12                <- @reboot crontab pulled the new HEAD unaided
WOL: Wake-on: g                          <- re-armed for the next cold wake
```

The wake -> current-OS guarantee is proven end to end: box powered off, one
magic packet, boots, auto-pulls main, claude (Max) and gh auth intact.

## Dial-in applied this session (root via passwordless sudo — see ADR-017 amendment)

- Lid switch: ignore on battery, external power, and docked; sleep, suspend,
  hibernate, and hybrid-sleep targets masked. The lid can be closed.
- WiFi: iwlwifi kernel module blacklisted (interface no longer exists);
  Bluetooth soft-blocked via rfkill.
- Firewall: ufw enabled and persistent — allow 22/tcp and tailscale0 only.
- Docker 29.1.3 installed, enabled, hello-world verified, safari in the
  docker group — unblocks Phase 2 M4 (in-container capsule execution).
- Already healthy, verified: netplan `wakeonlan: true` (WoL persistence),
  Tailscale up (keys valid to 2026-11-20), unattended-upgrades active, NTP
  synced, 857G free.
