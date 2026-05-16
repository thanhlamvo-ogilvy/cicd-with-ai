#!/usr/bin/env bash
# CI job: bandit
# Source: .github/workflows/backend-ci.yml
# Mirrors the "Check Bandit results" step — fails on HIGH or CRITICAL severity issues.
# Note: intentionally omits -o/--output flag to avoid writing bandit-report.json locally.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${BACKEND_DIR}"

if [ -f "${BACKEND_DIR}/.venv/bin/activate" ]; then
  # shellcheck source=/dev/null
  source "${BACKEND_DIR}/.venv/bin/activate"
fi

echo "▶ Running Bandit security scan..."
bandit -r app/ -c pyproject.toml -ll
echo "✅ Bandit security scan passed"
