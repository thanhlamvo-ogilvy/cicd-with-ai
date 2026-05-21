#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ENV_FILE="$SCRIPT_DIR/../.env"

if [[ -f "$ENV_FILE" ]]; then
  export $(grep -v '^#' "$ENV_FILE" | xargs)
fi

die() {
  echo "Error: $*" >&2
  exit 1
}


require_command() {
  local command_name="$1"

  if ! command -v "$command_name" >/dev/null 2>&1; then
    die "Required command not found: $command_name"
  fi
}



print_step() {
  local message="$1"
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "  ${message}"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

kill_port() {
  local port="$1"
  local pids
  pids=$(lsof -iTCP:"$port" -sTCP:LISTEN -t 2>/dev/null || true)
  if [[ -n "$pids" ]]; then
    echo "Killing process(es) on port $port: $pids"
    echo "$pids" | xargs kill -9 2>/dev/null || true
    sleep 1
  fi
}
