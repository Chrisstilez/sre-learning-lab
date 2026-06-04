#!/bin/bash
set -e

# Image tag comes from git commit SHA — never use "latest"
GIT_SHA=$(git rev-parse --short HEAD)
IMAGE_NAME="${DOCKER_REGISTRY:-christopher95}/sre-app"
IMAGE_TAG="${IMAGE_TAG_OVERRIDE:-$GIT_SHA}"

echo "=== STAGE: BUILD ==="
echo "Building image: ${IMAGE_NAME}:${IMAGE_TAG}"

docker build -t ${IMAGE_NAME}:${IMAGE_TAG} app/

echo ""
echo "✓ Build complete: ${IMAGE_NAME}:${IMAGE_TAG}"
