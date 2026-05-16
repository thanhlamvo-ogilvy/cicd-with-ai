#!/usr/bin/env bash
# CI job: pip-audit
# Source: .github/workflows/backend-ci.yml
# Mirrors the "Dependency Vulnerability Scan" job — uses two-call pattern matching CI:
#   first call prints output (|| true to not abort), second call exits non-zero on CVEs.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${BACKEND_DIR}"

if [ -f "${BACKEND_DIR}/.venv/bin/activate" ]; then
  # shellcheck source=/dev/null
  source "${BACKEND_DIR}/.venv/bin/activate"
fi

echo "▶ Running pip-audit dependency scan..."
pip-audit --skip-editable --desc || true
pip-audit --skip-editable --desc
echo "✅ Dependency scan passed — no high-severity CVEs found"
