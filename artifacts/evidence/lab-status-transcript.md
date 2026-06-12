# Evidence: labctl lab status — all green (2026-06-12)

Run from the Windows control plane against the live Lab box
(`labctl lab status`, one ssh round trip; ADR-017 operator bring-up):

```
[ok ] hostname: useragent
[ok ] uptime: up 2 hours, 27 minutes
[ok ] claude: 2.1.175 (Claude Code)
[ok ] codex: codex-cli 0.133.0
[ok ] gh_auth: ok
[ok ] repo_head: b56f613-2026-06-12
```

exit code: 0 — claude authed on the Max subscription
(verified separately: `claude auth status` reports loggedIn=true,
subscriptionType=max; `claude -p "say ok"` answered "OK"), gh authed as
Markus-Doc (repo/workflow/read:org), codex logged in via ChatGPT, repo
checkout current.
