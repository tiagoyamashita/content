#!/usr/bin/env bash
# Copy example skills and hooks to a target project root.
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 /path/to/your-project"
  exit 2
fi

TARGET="$1"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/.cursor"

if [[ ! -d "$SRC/skills" ]]; then
  echo "Error: expected $SRC/skills — run from examples/ folder"
  exit 1
fi

mkdir -p "$TARGET/.cursor/skills"
cp -r "$SRC/skills/"* "$TARGET/.cursor/skills/"
cp -r "$SRC/hooks" "$TARGET/.cursor/"
cp "$SRC/hooks.json" "$TARGET/.cursor/hooks.json"

GITIGNORE="$TARGET/.gitignore"
MARKER=".cursor/skills/*/logs/"
if [[ -f "$GITIGNORE" ]] && ! grep -qF "$MARKER" "$GITIGNORE" 2>/dev/null; then
  cat >>"$GITIGNORE" <<'EOF'

# Cursor skill/hook runtime logs
.cursor/skills/*/logs/
.cursor/hooks/logs/
EOF
  echo "Appended log paths to $GITIGNORE"
fi

echo "Copied skills and hooks to $TARGET/.cursor/"
echo "Smoke test:"
echo "  cd $TARGET && python3 .cursor/skills/deploy-check/scripts/deploy_check.py --environment staging --dry-run"
