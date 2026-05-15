#!/usr/bin/env bash
# CI job: ruff-lint
# Source: .github/workflows/backend-ci.yml
# Mirrors the "Ruff Lint" job — runs ruff check on the app package.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${BACKEND_DIR}"

if [ -f "${BACKEND_DIR}/.venv/bin/activate" ]; then
  # shellcheck source=/dev/null
  source "${BACKEND_DIR}/.venv/bin/activate"
fi

echo "▶ Running Ruff lint..."
ruff check app/
echo "✅ Ruff lint passed"
