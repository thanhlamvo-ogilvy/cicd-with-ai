#!/usr/bin/env bash
# scripts/build-pr-agent-config.sh
#
# Generates PR Agent configuration from AI-effective guideline sections.
# Only includes rules where AI adds unique value over linters and static analysis tools.
#
# Usage:
#   bash scripts/build-pr-agent-config.sh          # write .pr_agent.toml to repo root
#   bash scripts/build-pr-agent-config.sh --env    # write PR_AGENT_CONFIG to $GITHUB_ENV (for CI)

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUTPUT="$REPO_ROOT/.pr_agent.toml"

# Condensed review rules for AI — plain text, no markdown, no special chars.
# Content is sourced from openspec/specs/guidelines/ AI-effective sections.
review_rules() {
  cat <<'RULES'
You ARE A STRICT SENIOR ENGINEER REVIEWING A PULL REQUEST.

Focus ONLY on semantic, contextual, and cross-cutting concerns.
Automated CI tools (ruff, mypy, bandit, pip-audit) handle formatting, types, and lint.
Do NOT duplicate tool work — comments on formatting, type hints, or import order add noise without value.

BLOCK (Request Changes) for any of:

ARCHITECTURE & API DESIGN:
- Route handlers must be thin HTTP handlers; business logic belongs in service functions — reject logic in routes
- All list endpoints must support pagination (limit/offset or cursor); missing pagination must be flagged
- POST resource creation must return 201, DELETE must return 204, errors must use appropriate 4xx/5xx
- Every endpoint must declare a response_model; all errors must use {"detail": "message"} format
- PATCH endpoints must use payload.model_dump(exclude_unset=True) to distinguish absent from null
- POST endpoints must handle duplicate submissions gracefully

SCHEMA DESIGN:
- Every resource must follow the four-variant pattern: XxxBase, XxxCreate, XxxUpdate, XxxResponse
- XxxResponse must include model_config = ConfigDict(from_attributes=True) for ORM compatibility
- XxxUpdate fields must all be Optional — never required on a PATCH schema
- PATCH operations must use payload.model_dump(exclude_unset=True); omitted fields must remain unchanged

ERROR HANDLING:
- Bare except: without re-raising or specific exception type is forbidden
- Empty catch blocks that silently swallow errors are forbidden
- All network, database, and external service calls must have explicit timeouts
- Services must degrade gracefully (return cached data or fallback) when dependencies are unavailable
- Services must raise domain-specific exceptions; routes must catch and map them to HTTPException

SECURITY (contextual — bandit handles exact literal patterns separately):
- All DB queries must use SQLAlchemy ORM/Core with bound parameters; f-strings in SQL are forbidden
- JWT secrets and API keys must be loaded from settings (pydantic-settings via .env); hardcoded secrets forbidden
- Production error responses must not expose stack traces, DB error messages, or internal file paths
- Logs must not contain passwords, tokens, API keys, or PII

OBSERVABILITY:
- All logging must use structlog.get_logger(); print() and stdlib logging are forbidden
- Log entries must use structured context binding: log.info("event", key=value) not log.info(f"event {value}")
- AI provider calls must log only: provider, model, token_count, latency — never request/response bodies

PII & PRIVACY:
- Chat message content must never appear in log entries (log conversation_id and message_id only)
- CORS allow_methods must list specific HTTP methods in production config; wildcard ["*"] is forbidden

COMMIT MESSAGE FORMAT:
- Title: primary change first; "& more..." suffix if multi-topic; no trailing period
- Body: grouped under {PackageName} headers with present-tense action verb bullets; max 120 chars per bullet
- No dependency changes: include literal line "(No dependency updates.)"
- Never include Co-authored-by trailers or AI generator attribution

COMMENT (non-blocking) for:
- Endpoints missing both a positive (happy path) and a negative (error case) test
- Test names not following test_<action>_<expected_outcome> pattern
- PRs containing more than one logical change that should be split

IGNORE (CI tools handle these — do not comment):
- Code formatting, import order, line length (ruff)
- Type errors, missing annotations (mypy)
- Unused imports, dead code (ruff F401/F841)
- eval()/exec() exact patterns (bandit B307)
- Hardcoded password string literals (bandit B105/B106)
- SQL injection via string literal patterns (bandit B608)
- CVE vulnerabilities in dependencies (pip-audit, Dependabot)
- Test coverage percentage (pytest --cov)
RULES
}

suggestion_rules() {
  cat <<'RULES'
Suggest code improvements only for:
- Security: contextual violations (missing auth checks, unsafe SQL patterns, PII exposure)
- Error handling: missing timeouts, swallowed exceptions, absent graceful degradation
- Schema design: missing ConfigDict, non-Optional PATCH fields, incomplete schema variants
- Logging correctness: print() usage, f-string log formatting, sensitive data in logs
- API design completeness: missing response_model, missing pagination, wrong status codes

Maximum 3 suggestions. Be specific with code examples. Focus on correctness over style.
Do NOT suggest changes to formatting, type hints, or import structure — CI tools handle those.
RULES
}

generate_toml() {
  cat <<'STATIC_TOP'
[config]
model = "gpt-5.4"

[pr_reviewer]
require_score_review = true
inline_code_comments = true
num_code_suggestions = 3

extra_instructions = """
STATIC_TOP
  review_rules
  cat <<'STATIC_MID'
"""

[pr_code_suggestions]
num_code_suggestions = 3

extra_instructions = """
STATIC_MID
  suggestion_rules
  printf '"""\n'
}

if [[ "${1:-}" == "--env" ]]; then
  if [[ -z "${GITHUB_ENV:-}" ]]; then
    echo "❌ GITHUB_ENV is not set — the --env flag is for GitHub Actions only" >&2
    exit 1
  fi
  {
    echo "PR_AGENT_CONFIG<<__AGENT_EOF__"
    generate_toml
    echo "__AGENT_EOF__"
  } >> "$GITHUB_ENV"
  echo "✅ PR_AGENT_CONFIG written to \$GITHUB_ENV"
else
  generate_toml > "$OUTPUT"
  echo "✅ Generated $OUTPUT"
fi
