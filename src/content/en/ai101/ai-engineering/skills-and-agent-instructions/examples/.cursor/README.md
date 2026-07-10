# Skills & hooks examples

Copy-ready `.cursor/` layout for the [Skills examples](../) docs. All paths use **`.cursor/`** at your project root.

## Layout

```text
.cursor/
  hooks.json
  hooks/
    secrets_scan.py
    lib/
      scan_staged_secrets.py
      scan_staged_secrets_cli.py
    logs/                    ← created at runtime; gitignored
  skills/
    deploy-check/
    test-flake-hunt/
    perf-scan/
    secrets-scan-help/
```

## Copy to your project

From this `examples/` folder:

```bash
# Run from: .../skills-and-agent-instructions/examples/
mkdir -p /path/to/your-project/.cursor/skills
cp -r .cursor/skills/* /path/to/your-project/.cursor/skills/
cp -r .cursor/hooks /path/to/your-project/.cursor/
cp .cursor/hooks.json /path/to/your-project/.cursor/hooks.json
```

Or use the helper script:

```bash
./scripts/copy-to-project.sh /path/to/your-project
```

Add to your project `.gitignore`:

```gitignore
.cursor/skills/*/logs/
.cursor/hooks/logs/
```

## Smoke test (after copy)

```bash
cd /path/to/your-project
python3 .cursor/skills/deploy-check/scripts/deploy_check.py --environment staging --dry-run
```

Expect: `Log written: .../deploy-check/logs/run-….json`

## Requirements

| Item | Need |
|------|------|
| Python | 3.10+ (stdlib only) |
| deploy-check | Optional `STAGING_URL` env var |
| test-flake-hunt | `npm test` in your project |
| perf-scan | Codebase to scan; optional `PERF_URL` |
| secrets hook | Git repo; `python3` on PATH when Cursor runs hooks |

## Wire hooks in Cursor

`hooks.json` is included. Cursor loads `.cursor/hooks.json` from the project root. Restart Cursor or save the file if hooks do not appear — check **Settings → Hooks**.

Test hook manually:

```bash
echo '{"command":"git commit -m test"}' | python3 .cursor/hooks/secrets_scan.py
```

## Optional: git pre-commit

```bash
chmod +x .cursor/hooks/lib/scan_staged_secrets_cli.py
# .git/hooks/pre-commit
#!/bin/sh
cd "$(git rev-parse --show-toplevel)" || exit 1
exec python3 .cursor/hooks/lib/scan_staged_secrets_cli.py
```
