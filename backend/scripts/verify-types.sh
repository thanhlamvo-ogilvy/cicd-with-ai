#!/usr/bin/env bash
# CI job: mypy
# Source: .github/workflows/backend-ci.yml
# Mirrors the "Type Check (Mypy)" job — runs strict type checking.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${BACKEND_DIR}"

if [ -f "${BACKEND_DIR}/.venv/bin/activate" ]; then
  # shellcheck source=/dev/null
  source "${BACKEND_DIR}/.venv/bin/activate"
fi

echo "▶ Running Mypy type check..."
mypy app/ --strict
echo "✅ Mypy type check passed"
