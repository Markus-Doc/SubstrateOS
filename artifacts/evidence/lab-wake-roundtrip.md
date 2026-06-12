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

## Addendum (same day): suspend-only lifecycle + boot-to-agent

Wake-from-S5 proved unreliable in repeat testing (one success, then two
failures needing the physical power button) — BIOS-level, not fixable from
the OS. Policy changed to **suspend-only** (ADR-017 §5):

```
$ labctl lab sleep
suspend sent to substrate-lab (resume with `labctl lab wake`)
$ labctl lab wake --wait     # subnet-directed broadcast, burst of 3
lab host is reachable        # 16.3s
$ labctl lab sleep && labctl lab wake --wait
lab host is reachable        # 16.1s  (repeatable)
```

Root cause of flaky wakes: 255.255.255.255 leaves a nondeterministic
interface on the multi-homed control plane; LAB_WOL_BROADCAST now pins the
subnet-directed broadcast.

Boot-to-agent verified end to end: `substrateos-agent.service` pulls the
repo and starts `claude --dangerously-skip-permissions` in tmux session
`substrateos` at every boot. After a cold boot the standing session answered
the liveness prompt unaided, and the same session (created at boot) survived
two suspend/resume cycles intact.
