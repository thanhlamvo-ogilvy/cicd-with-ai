#!/usr/bin/env bash
# CI job: pytest
# Source: .github/workflows/backend-ci.yml
# Mirrors the "Tests & Coverage" job — runs pytest with coverage reporting.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${BACKEND_DIR}"

if [ -f "${BACKEND_DIR}/.venv/bin/activate" ]; then
  # shellcheck source=/dev/null
  source "${BACKEND_DIR}/.venv/bin/activate"
fi

echo "▶ Running tests with coverage..."
pytest tests/ -v --cov=app --cov-report=term-missing --cov-report=html
echo "✅ Tests passed"
