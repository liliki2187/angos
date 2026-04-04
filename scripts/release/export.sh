#!/usr/bin/env bash
# Godot 4 headless export for CI
# Usage: ./export.sh <preset> <output-path>

set -euo pipefail

PRESET="${1:-Windows Desktop}"
OUTPUT="${2:-build/game.exe}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PROJECT_ROOT="$REPO_ROOT/gd_project"

# Find Godot binary
GODOT=$(which godot4 2>/dev/null || which godot 2>/dev/null || echo "")
if [[ -z "$GODOT" ]]; then
  echo "ERROR: godot4 or godot not found in PATH"
  exit 1
fi

if [[ ! -f "$PROJECT_ROOT/project.godot" ]]; then
  echo "ERROR: gd_project/project.godot not found"
  exit 1
fi

echo "Building with $GODOT — preset: $PRESET → gd_project/$OUTPUT"
"$GODOT" --headless --path "$PROJECT_ROOT" --export-release "$PRESET" "$OUTPUT"
echo "Build OK: gd_project/$OUTPUT"
