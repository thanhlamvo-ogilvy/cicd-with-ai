#!/usr/bin/env bash
# Recreate only the PR Agent container so .pr_agent.toml changes are reloaded,
# while keeping the ngrok tunnel service available.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
COMPOSE_FILE="${REPO_ROOT}/docker-compose-pragent.yml"

PR_AGENT_SERVICE="pr-agent"
NGROK_SERVICE="ngrok"

# shellcheck source=scripts/_common.sh
source "${SCRIPT_DIR}/_common.sh"

require_command docker

if [[ ! -f "${COMPOSE_FILE}" ]]; then
  die "Compose file not found: ${COMPOSE_FILE}"
fi

print_step "Checking ngrok status before restart"
ngrok_was_running="false"
if docker compose -f "${COMPOSE_FILE}" ps --status running "${NGROK_SERVICE}" | grep -q "${NGROK_SERVICE}"; then
  ngrok_was_running="true"
  echo "ngrok is running."
else
  echo "ngrok is not currently running."
fi

print_step "Restarting only pr-agent service"
docker compose -f "${COMPOSE_FILE}" up -d --no-deps --force-recreate "${PR_AGENT_SERVICE}"

print_step "Verifying service states"
docker compose -f "${COMPOSE_FILE}" ps "${PR_AGENT_SERVICE}" "${NGROK_SERVICE}"

if [[ "${ngrok_was_running}" == "true" ]]; then
  if docker compose -f "${COMPOSE_FILE}" ps --status running "${NGROK_SERVICE}" | grep -q "${NGROK_SERVICE}"; then
    echo "ngrok is still running."
  else
    echo "ngrok stopped unexpectedly; starting it again..."
    docker compose -f "${COMPOSE_FILE}" up -d "${NGROK_SERVICE}"
  fi
fi

echo ""
echo "Done. PR Agent has been recreated and config changes from .pr_agent.toml are now applied."