#!/usr/bin/env bash
# Show active PR Agent configuration without posting any PR comment.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SERVICE_NAME="pr-agent-github"

# shellcheck source=scripts/_common.sh
source "${SCRIPT_DIR}/_common.sh"

require_command docker

print_step "Checking PR Agent container"
if ! docker ps --format '{{.Names}}' | grep -qx "${SERVICE_NAME}"; then
  die "Container '${SERVICE_NAME}' is not running. Start with: docker compose -f docker-compose-pragent.yml up -d"
fi

print_step "Mounted file-based config (.secrets.toml)"
docker exec "${SERVICE_NAME}" sh -lc '
if [ -f /app/pr_agent/settings/.secrets.toml ]; then
  cat /app/pr_agent/settings/.secrets.toml
else
  echo "No /app/pr_agent/settings/.secrets.toml found"
fi
'

print_step "Environment overrides (highest precedence)"
docker exec "${SERVICE_NAME}" sh -lc '
env | sort | grep -E "^(CONFIG__|IGNORE__|OPENAI__|OPENAI_|GITHUB__|GITHUB_APP__)" | \
  sed -E "s/^(([^=]*(TOKEN|KEY|SECRET)[^=]*)=).*/\1<redacted>/I" || true
'

echo ""
echo "Done. This output is local only and does not post to GitHub PR comments."