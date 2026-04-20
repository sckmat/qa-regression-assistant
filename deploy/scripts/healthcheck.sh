#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEPLOY_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd "${DEPLOY_DIR}"

set -a
source ./env/runtime.env
set +a

echo "Checking local reverse proxy..."
curl -fsS -H "Host: ${PUBLIC_DOMAIN}" http://127.0.0.1/ >/dev/null

echo "Checking public API health..."
curl -fsS "https://${PUBLIC_DOMAIN}/api/v1/health/live" >/dev/null

echo "Checking containers..."
docker compose --env-file ./env/runtime.env -f ./docker-compose.prod.yml ps

echo "Healthcheck passed"