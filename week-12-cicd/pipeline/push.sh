#!/bin/bash
set -e

GIT_SHA=$(git rev-parse --short HEAD)
IMAGE_NAME="${DOCKER_REGISTRY:-christopher95}/sre-app"
IMAGE_TAG="${IMAGE_TAG_OVERRIDE:-$GIT_SHA}"

echo "=== STAGE: PUSH ==="
echo "Pushing image: ${IMAGE_NAME}:${IMAGE_TAG}"

docker push ${IMAGE_NAME}:${IMAGE_TAG}

echo ""
echo "✓ Push complete: ${IMAGE_NAME}:${IMAGE_TAG}"
