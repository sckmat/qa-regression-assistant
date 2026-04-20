#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: bash scripts/deploy.sh <image_tag>"
  exit 1
fi

IMAGE_TAG_OVERRIDE="$1"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEPLOY_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd "${DEPLOY_DIR}"

if [[ ! -f ./env/runtime.env ]]; then
  echo "Missing ./env/runtime.env"
  exit 1
fi

export IMAGE_TAG="${IMAGE_TAG_OVERRIDE}"

echo "Generating runtime env files..."
bash ./scripts/render-env.sh

echo "Pulling images with tag: ${IMAGE_TAG}"
docker compose --env-file ./env/runtime.env -f ./docker-compose.prod.yml pull

echo "Running migrations..."
bash ./scripts/migrate.sh

echo "Starting services..."
docker compose --env-file ./env/runtime.env -f ./docker-compose.prod.yml up -d caddy frontend user_service data_service

set -a
source ./env/runtime.env
set +a

if [[ "${ENABLE_LLM}" == "true" ]]; then
  echo "Starting llm profile..."
  docker compose --env-file ./env/runtime.env -f ./docker-compose.prod.yml --profile llm up -d llm_service
fi

echo "Running health checks..."
bash ./scripts/healthcheck.sh

echo "Deploy completed successfully"