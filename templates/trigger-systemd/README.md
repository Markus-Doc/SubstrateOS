# Remote Trigger systemd Template

## What this is

The systemd unit that runs the SubstrateOS remote trigger duty cycle (ADR-018) on the
Lab box. At boot, systemd starts `labctl trigger cycle`: the loop long-polls the
Telegram Bot API (outbound HTTPS only, no inbound port), drains the command queue,
executes any mission through the established capsule machinery (ADR-015/016), replies
on the same chat, then re-suspends the host with the next RTC alarm armed. Any resume —
RTC alarm or Wake-on-LAN magic packet — returns control to the same loop, so one
enabled unit survives reboot and suspend alike.

## Placeholder tokens (substituted by `labctl trigger install`)

| Token | Replaced with |
|---|---|
| `__TRIGGER_USER__` | The Unix user the cycle runs as (the owner's login user on the box) |
| `__TRIGGER_REPO__` | Absolute path of the SubstrateOS checkout on the box (also the working directory, and where the gitignored `.env` lives) |
| `__TRIGGER_VENV__` | Absolute path of the virtualenv whose `bin/labctl` provides the `trigger` command group |
| `__TRIGGER_HOME__` | The owner's home directory, so the unit's `PATH` reaches `~/.local/bin` — systemd's default PATH does not, and that is where the `claude` CLI missions need lives |

## Install

On the box, from the repo checkout:

```bash
.venv/bin/labctl trigger install
```

This substitutes the three tokens from the live environment, writes the unit to
`/etc/systemd/system/substrateos-trigger.service`, and enables it.

Manual fallback (equivalent, if you prefer to see every step):

```bash
sed -e "s|__TRIGGER_USER__|$USER|g" \
    -e "s|__TRIGGER_REPO__|$HOME/SubstrateOS|g" \
    -e "s|__TRIGGER_VENV__|$HOME/SubstrateOS/.venv|g" \
    -e "s|__TRIGGER_HOME__|$HOME|g" \
    templates/trigger-systemd/substrateos-trigger.service \
  | sudo tee /etc/systemd/system/substrateos-trigger.service >/dev/null
sudo systemctl daemon-reload
sudo systemctl enable --now substrateos-trigger.service
```

## Why `ConditionPathExists` guards `.env`

All machine-specific trigger configuration (`TRIGGER_TELEGRAM_TOKEN`,
`TRIGGER_ALLOWED_USER_IDS`) lives in the gitignored `.env` at the repo root — never in
tracked files. A box with no `.env` has never been configured at all, so there is
nothing the cycle could do. systemd treats a failed `ConditionPathExists` as a skip,
not a failure: the unit stays enabled with no error state and starts normally on the
first boot after `.env` exists.

## Not-configured behaviour (exit 0)

If `.env` exists but the trigger keys are absent (the box is set up for the Lab
operator channel but not yet for the trigger), `labctl trigger cycle` reports
not-configured and exits 0. Because the unit uses `Restart=on-failure`, a clean exit
is final: systemd does not respawn-loop a half-configured box. Add the keys to `.env`
and `sudo systemctl restart substrateos-trigger.service` (or just reboot) to bring the
pathway up.
