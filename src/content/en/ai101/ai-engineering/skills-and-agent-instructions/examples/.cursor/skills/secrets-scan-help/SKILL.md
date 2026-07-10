---
name: secrets-scan-help
description: Explain secrets-scan hook failures and how to fix staged .env or leaked keys. Use when commit blocked, secrets scan failed, or .env staged.
---

# Secrets scan failures

1. Read latest log in `.cursor/hooks/logs/secrets-scan-*.json`.
2. For `STAGED_ENV_FILE`: unstage with `git reset HEAD -- <file>`; ensure `.env` is in `.gitignore`.
3. For `POSSIBLE_SECRET_IN_STAGED_DIFF`: rotate the secret; remove from code; use env vars.
4. Never tell the user to commit secrets to "fix" the hook.
