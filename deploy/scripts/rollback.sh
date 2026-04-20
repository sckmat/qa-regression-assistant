#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: bash scripts/rollback.sh <old_image_tag>"
  exit 1
fi

OLD_TAG="$1"

echo "Rolling back to tag: ${OLD_TAG}"
bash "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/deploy.sh" "${OLD_TAG}"