#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEPLOY_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd "${DEPLOY_DIR}"

set -a
source ./env/runtime.env
set +a

if [[ ! -f ./env/user_service.env || ! -f ./env/data_service.env ]]; then
  echo "Runtime env files are missing. Run scripts/render-env.sh first."
  exit 1
fi

if [[ -n "${USER_SERVICE_MIGRATE_COMMAND:-}" ]]; then
  echo "Running user_service migrations..."
  docker compose --env-file ./env/runtime.env -f ./docker-compose.prod.yml run --rm --no-deps \
    user_service sh -lc "${USER_SERVICE_MIGRATE_COMMAND}"
else
  echo "Skipping user_service migrations"
fi

if [[ -n "${DATA_SERVICE_MIGRATE_COMMAND:-}" ]]; then
  echo "Running data_service migrations..."
  docker compose --env-file ./env/runtime.env -f ./docker-compose.prod.yml run --rm --no-deps \
    data_service sh -lc "${DATA_SERVICE_MIGRATE_COMMAND}"
else
  echo "Skipping data_service migrations"
fi