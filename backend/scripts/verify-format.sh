#!/usr/bin/env bash
# CI job: ruff-format
# Source: .github/workflows/backend-ci.yml
# Mirrors the "Ruff Format" job — checks code formatting without modifying files.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${BACKEND_DIR}"

if [ -f "${BACKEND_DIR}/.venv/bin/activate" ]; then
  # shellcheck source=/dev/null
  source "${BACKEND_DIR}/.venv/bin/activate"
fi

echo "▶ Checking code formatting..."
ruff format --check app/
echo "✅ Ruff format check passed"
