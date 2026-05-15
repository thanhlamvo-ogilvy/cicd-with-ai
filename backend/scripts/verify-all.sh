#!/usr/bin/env bash
# CI job: status-check (combined runner)
# Source: .github/workflows/backend-ci.yml
# Runs all six verify scripts sequentially, collects results, and prints a
# named pass/fail summary. Does NOT exit on first failure — all checks run.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

CHECKS=("lint" "format" "types" "security" "tests" "deps")
SCRIPTS=(
  "${SCRIPT_DIR}/verify-lint.sh"
  "${SCRIPT_DIR}/verify-format.sh"
  "${SCRIPT_DIR}/verify-types.sh"
  "${SCRIPT_DIR}/verify-security.sh"
  "${SCRIPT_DIR}/verify-tests.sh"
  "${SCRIPT_DIR}/verify-deps.sh"
)

RESULTS=()
FAILED=0

for i in "${!CHECKS[@]}"; do
  name="${CHECKS[$i]}"
  script="${SCRIPTS[$i]}"

  echo ""
  echo "══════════════════════════════════════════"
  echo "  Running: ${name}"
  echo "══════════════════════════════════════════"

  if bash "${script}"; then
    RESULTS+=("PASSED")
  else
    RESULTS+=("FAILED")
    FAILED=1
  fi
done

echo ""
echo "══════════════════════════════════════════"
echo "  CI Verification Summary"
echo "══════════════════════════════════════════"
for i in "${!CHECKS[@]}"; do
  name="${CHECKS[$i]}"
  result="${RESULTS[$i]}"
  if [ "${result}" = "PASSED" ]; then
    echo "  ✅ ${name}: PASSED"
  else
    echo "  ❌ ${name}: FAILED"
  fi
done
echo "══════════════════════════════════════════"

if [ "${FAILED}" -eq 0 ]; then
  echo "  ✅ All checks passed"
  echo "══════════════════════════════════════════"
  exit 0
else
  echo "  ❌ One or more checks failed"
  echo "══════════════════════════════════════════"
  exit 1
fi
