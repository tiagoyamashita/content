# Skills & hooks examples

Runnable reference layout for the [Skills examples](../) docs.

## Layout

```text
examples/.cursor/
  hooks.json
  hooks/
    secrets_scan.py
    lib/
  skills/
    deploy-check/
    test-flake-hunt/
    perf-scan/
    secrets-scan-help/
```

## Use in this repo (docs)

Run scripts from the **content repo root**:

```bash
python3 src/content/en/ai101/ai-engineering/skills-and-agent-instructions/examples/.cursor/skills/deploy-check/scripts/deploy_check.py \
  --environment staging --dry-run
```

Paths in each `SKILL.md` use the shorter prefix `examples/.cursor/...` — adjust if your cwd differs.

## Copy to your project

```bash
cp -r examples/.cursor/skills/* .cursor/skills/
cp -r examples/.cursor/hooks .cursor/
cp examples/.cursor/hooks.json .cursor/hooks.json
```

Then update paths in `SKILL.md` and `hooks.json` from `examples/.cursor/` to `.cursor/`.

## Wire hooks in Cursor

Copy `hooks.json` to your repo `.cursor/hooks.json` (or merge entries). Cursor loads project hooks from `.cursor/hooks.json`.
