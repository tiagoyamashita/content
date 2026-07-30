---
label: "IV"
subtitle: "Hook — secrets & env scan"
group: "Skills examples"
order: 4
---
Hook — secrets & `.env` scan

**Goal:** A **bot** that runs on **hooks** — before shell runs `git commit` — and scans for exposed secrets, `.env` files staged, API keys in diffs. Writes a **log**; can **block** the action when `failClosed` is set.

Hooks run **automatically**; skills run when the user asks. See [Linking a fixed script](../../iv-cursor-skills-rules-agents-md.md#linking-a-fixed-script).

## Live files (copy-ready)

| File | Path |
|------|------|
| Hook config | [`.cursor/hooks.json`](.cursor/hooks.json) |
| Hook script | [`.cursor/hooks/secrets_scan.py`](.cursor/hooks/secrets_scan.py) |
| Scan logic | [`.cursor/hooks/lib/scan_staged_secrets.py`](.cursor/hooks/lib/scan_staged_secrets.py) |
| Pre-commit CLI | [`.cursor/hooks/lib/scan_staged_secrets_cli.py`](.cursor/hooks/lib/scan_staged_secrets_cli.py) |
| Help skill | [`.cursor/skills/secrets-scan-help/SKILL.md`](.cursor/skills/secrets-scan-help/SKILL.md) |

Copy all of [`.cursor/`](.cursor/README.md) to your project root.

## Folder layout

```text
.cursor/
  hooks.json
  hooks/
    secrets_scan.py
    lib/
    logs/
```

## Hook config

See [`.cursor/hooks.json`](.cursor/hooks.json) — `beforeShellExecution` on `git\s+commit`, `failClosed: true`.

Test manually:

```bash
echo '{"command":"git commit -m test"}' | python3 .cursor/hooks/secrets_scan.py
```

## Optional: git pre-commit

```bash
chmod +x .cursor/hooks/lib/scan_staged_secrets_cli.py
# .git/hooks/pre-commit → exec python3 .cursor/hooks/lib/scan_staged_secrets_cli.py
```

## Agent / user flow

```text
User or agent: git commit -m "…"
  → beforeShellExecution fires
  → secrets_scan.py runs → writes log
  → exit 2 → commit blocked (if failClosed)
  → secrets-scan-help skill → read log → suggest fixes
```

## Next

[Performance & bottlenecks](v-performance-bottleneck-scan.md) — on-demand profiling skill.
