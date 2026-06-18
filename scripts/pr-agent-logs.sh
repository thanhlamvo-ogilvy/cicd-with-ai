#!/usr/bin/env bash
# Stream live logs from the PR Agent container.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
COMPOSE_FILE="${REPO_ROOT}/docker-compose-pragent.yml"
SERVICE_NAME="pr-agent"

# shellcheck source=scripts/_common.sh
source "${SCRIPT_DIR}/_common.sh"

require_command docker

if [[ ! -f "${COMPOSE_FILE}" ]]; then
  die "Compose file not found: ${COMPOSE_FILE}"
fi

FOLLOW=true
TAIL_LINES="200"
SINCE=""

usage() {
  cat <<'EOF'
Usage: scripts/pr-agent-logs.sh [OPTIONS]

Stream PR Agent logs.

Options:
  --no-follow         Show logs and exit
  --tail <n>          Number of lines from the end of logs (default: 200)
  --since <duration>  Show logs since duration (e.g. 10m, 1h)
  --help, -h          Show help

Examples:
  scripts/pr-agent-logs.sh
  scripts/pr-agent-logs.sh --tail 50
  scripts/pr-agent-logs.sh --since 15m
  scripts/pr-agent-logs.sh --no-follow --tail 100
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --no-follow)
      FOLLOW=false
      shift
      ;;
    --tail)
      if [[ $# -lt 2 ]]; then
        die "--tail requires a numeric value"
      fi
      TAIL_LINES="$2"
      shift 2
      ;;
    --since)
      if [[ $# -lt 2 ]]; then
        die "--since requires a duration value"
      fi
      SINCE="$2"
      shift 2
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      die "Unknown argument: $1"
      ;;
  esac
done

log_args=("-f" "${COMPOSE_FILE}" "logs" "--tail" "${TAIL_LINES}")

if [[ -n "${SINCE}" ]]; then
  log_args+=("--since" "${SINCE}")
fi

if [[ "${FOLLOW}" == "true" ]]; then
  log_args+=("-f" "${SERVICE_NAME}")
else
  log_args+=("${SERVICE_NAME}")
fi

docker compose "${log_args[@]}"