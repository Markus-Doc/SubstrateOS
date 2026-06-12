# Evidence: labctl lab dispatch + wake — Lab operator user-ready (2026-06-12)

All commands run from the Windows control plane against the live Lab box
(ADR-017 operator bring-up, M2 of the realigned Phase 2 plan).

## Metered dispatch demo (real mission, Max subscription)

Mission: create `HELLO.md` with one line and report — run in `~/lab-scratch`
on the box (a scratch dir, NOT the SubstrateOS checkout).

```
$ labctl lab dispatch "Create a file named HELLO.md ..." --workdir '~/lab-scratch'
run log: artifacts\lab-runs\run-20260612T092401Z.jsonl
tokens used: 21334 / budget 2000000
dispatch completed within budget
exit=0
```

Verification on the box: `cat ~/lab-scratch/HELLO.md` →
`Hello from the SubstrateOS Lab operator.` — and the agent's stream-json
result event reports `/home/safari/lab-scratch/HELLO.md`. The full metered
run log (7 stream-json events, usage fields present) is committed alongside
as `lab-dispatch-demo-run.jsonl`. Auth was subscription-only: claude
`loggedIn=true, subscriptionType=max`; no API key anywhere.

Found and fixed during the demo: click on Windows pre-expands `~` in argv
(`click.utils._expand_args`), so `--workdir '~/lab-scratch'` arrived as the
LOCAL Windows home. `labctl.lab._unexpand_local_home` maps it back to the
remote home (unit-tested).

## Wake

```
$ labctl lab wake --wait --timeout 60
magic packet sent (broadcast 255.255.255.255:9)
waiting for ssh on substrate-lab (timeout 60s)...
lab host is reachable
exit=0
```

The packet fires and ssh answers. A full power-cycle round trip (box OFF →
wake → ssh) was NOT exercised this session: the operator account has no
sudo and `systemctl reboot` over ssh is denied by polkit ("Interactive
authentication required"). Owner can complete it anytime: shut the box
down, then `labctl lab wake --wait`. WoL is confirmed enabled in firmware
(`Wake-on: g`).

## Sync

```
$ labctl lab sync
lab repo HEAD: b56f613-2026-06-12
exit=0
```
