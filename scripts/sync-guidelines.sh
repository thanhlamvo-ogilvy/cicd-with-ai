#!/usr/bin/env bash
# scripts/sync-guidelines.sh
#
# Regenerates .github/copilot-review-instructions.md from AI-effective guideline sections.
# Only includes rules that benefit from AI review — excludes checks that linters and
# static analysis tools (ruff, mypy, bandit, pip-audit) already enforce.
#
# Usage:
#   bash scripts/sync-guidelines.sh           # regenerate the file
#   bash scripts/sync-guidelines.sh --check   # exit 1 if file would change (for CI)

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
GUIDELINES="$REPO_ROOT/openspec/specs/guidelines"
OUTPUT="$REPO_ROOT/.github/copilot-review-instructions.md"

# Extract the content of a named ## section from a guideline file.
# Starts printing after the matching header line, stops at the next ## header.
section() {
  local file="$1" header="$2"
  awk -v hdr="## ${header}" '$0==hdr{p=1;next} /^## /{if(p)exit} p{print}' "$file"
}

generate() {
  cat <<'HEADER'
<!--
AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
Source: openspec/specs/guidelines/
Regenerate with: bash scripts/sync-guidelines.sh
-->

# Copilot Code Review Instructions

> These instructions define what GitHub Copilot reviews in pull requests.
> **Scope:** Only semantic, contextual, and cross-cutting concerns that automated tools cannot catch.
> CI tools (ruff, mypy, bandit, pip-audit) handle all mechanical/syntactic checks — do not duplicate their work.

## What Automated Tools Already Handle (Do Not Review)

| Concern | Tool |
|---|---|
| Code formatting, import order, line length | ruff (format + I + E/W) |
| Type errors, missing type annotations | mypy |
| Unused imports, dead code | ruff (F401, F841) |
| `eval()` / `exec()` usage | bandit (B307) |
| Hardcoded password string literals | bandit (B105, B106) |
| SQL injection via string literal patterns | bandit (B608) |
| Known CVE vulnerabilities in dependencies | pip-audit, Dependabot |
| Test coverage percentage | pytest --cov |
| React hooks violations | ESLint |

---

## Block (Request Changes) Rules

### Architecture & API Design

HEADER

  section "$GUIDELINES/backend-api-design/spec.md" "Architecture"
  echo ""
  section "$GUIDELINES/backend-api-design/spec.md" "HTTP Status Codes"
  echo ""
  section "$GUIDELINES/backend-api-design/spec.md" "Response & Error Format"
  echo ""
  section "$GUIDELINES/backend-api-design/spec.md" "List Endpoints"
  echo ""
  section "$GUIDELINES/backend-api-design/spec.md" "Mutations"
  echo ""

  cat <<'SCHEMA_HEADER'
### Schema Design

SCHEMA_HEADER

  section "$GUIDELINES/backend-schema-design/spec.md" "Pydantic Schema Pattern"
  echo ""
  section "$GUIDELINES/backend-schema-design/spec.md" "Partial Updates"
  echo ""
  section "$GUIDELINES/backend-schema-design/spec.md" "SQLAlchemy Models"
  echo ""

  cat <<'ERROR_HEADER'
### Error Handling

> Note: bare `except:` patterns are a hint, but focus on semantic violations — swallowed errors,
> missing timeouts on external calls, and missing graceful degradation that no tool can detect.

ERROR_HEADER

  section "$GUIDELINES/shared-error-handling/spec.md" "Exception Handling"
  echo ""
  section "$GUIDELINES/shared-error-handling/spec.md" "Retries & Timeouts"
  echo ""
  section "$GUIDELINES/shared-error-handling/spec.md" "Resilience"
  echo ""
  section "$GUIDELINES/shared-error-handling/spec.md" "Backend: Domain Exceptions → HTTP Errors"
  echo ""

  cat <<'SECURITY_HEADER'
### Security

> Note: `eval()`/`exec()` exact patterns and hardcoded password string literals are caught by bandit.
> Focus on contextual violations: ORM usage in DB queries, secrets loaded from config, safe error responses.

SECURITY_HEADER

  section "$GUIDELINES/backend-security-owasp/spec.md" "SQL Injection Prevention"
  echo ""
  section "$GUIDELINES/backend-security-owasp/spec.md" "Password & Secret Handling"
  echo ""
  section "$GUIDELINES/backend-security-owasp/spec.md" "Error Responses"
  echo ""
  section "$GUIDELINES/backend-security-owasp/spec.md" "Logs"
  echo ""

  cat <<'OBS_HEADER'
### Observability & Logging

OBS_HEADER

  section "$GUIDELINES/backend-observability/spec.md" "Logging"
  echo ""
  section "$GUIDELINES/backend-observability/spec.md" "Sensitive Data in Logs"
  echo ""

  cat <<'PII_HEADER'
### PII & Data Privacy

PII_HEADER

  section "$GUIDELINES/ai-chat-pii/spec.md" "Log Sanitization"
  echo ""
  section "$GUIDELINES/ai-chat-pii/spec.md" "CORS & Auth Hardening"
  echo ""

  cat <<'GIT_HEADER'
### Commit Message Format

GIT_HEADER

  section "$GUIDELINES/shared-git-workflow/spec.md" "Commit Message Format"
  echo ""

  cat <<'FOOTER'
---

## Comment (Non-Blocking) Rules

- Flag endpoints that lack both a positive (happy path) **and** a negative (error case) test
- Flag test function names that do not follow `test_<action>_<expected_outcome>` pattern
- Flag PRs that contain more than one logical change and should be split
- Suggest graceful degradation where a dependency failure would crash the service rather than degrade

---

## Ignore (Handled by Automated Tools)

Do not comment on anything listed in the **What Automated Tools Already Handle** table above.
Do not comment on code style, formatting, naming conventions, or type annotations.
These are enforced by ruff, mypy, bandit, and other CI tools — duplicate comments add noise without value.
FOOTER
}

if [[ "${1:-}" == "--check" ]]; then
  actual=$(cat "$OUTPUT" 2>/dev/null || true)
  expected=$(generate)
  if [[ "$actual" == "$expected" ]]; then
    echo "✅ $OUTPUT is up to date"
  else
    echo "❌ $OUTPUT is out of sync with guidelines" >&2
    echo "   Run: bash scripts/sync-guidelines.sh" >&2
    exit 1
  fi
else
  generate > "$OUTPUT"
  echo "✅ Generated $OUTPUT"
fi
