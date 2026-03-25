#!/usr/bin/env bash
# Godot 4 headless export for CI
# Usage: ./export.sh <preset> <output-path>

set -euo pipefail

PRESET="${1:-Windows Desktop}"
OUTPUT="${2:-build/game.exe}"

# Find Godot binary
GODOT=$(which godot4 2>/dev/null || which godot 2>/dev/null || echo "")
if [[ -z "$GODOT" ]]; then
  echo "ERROR: godot4 or godot not found in PATH"
  exit 1
fi

echo "Building with $GODOT — preset: $PRESET → $OUTPUT"
"$GODOT" --headless --export-release "$PRESET" "$OUTPUT"
echo "Build OK: $OUTPUT"
