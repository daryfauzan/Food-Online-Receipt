#!/usr/bin/env bash
set -euo pipefail

# Default path is current directory
TARGET_PATH=${1:-"."}

echo "🔍 Running Ruff linter on $TARGET_PATH ..."

# Run Ruff linting
ruff check "$TARGET_PATH"

# Optionally, also run Ruff formatter (comment out if not needed)
# echo "✨ Running Ruff formatter on $TARGET_PATH ..."
# ruff format "$TARGET_PATH"

echo "✅ Linting complete."