#!/bin/bash
set -e

GIT_SHA=$(git rev-parse --short HEAD)
IMAGE_NAME="${DOCKER_REGISTRY:-christopher95}/sre-app"
IMAGE_TAG="${IMAGE_TAG_OVERRIDE:-$GIT_SHA}"
NAMESPACE="${DEPLOY_NAMESPACE:-default}"

echo "=== STAGE: DEPLOY ==="
echo "Deploying ${IMAGE_NAME}:${IMAGE_TAG} to namespace ${NAMESPACE}"

# Substitute the image tag into the manifest
sed "s|IMAGE_PLACEHOLDER|${IMAGE_NAME}:${IMAGE_TAG}|g" k8s/deployment.yaml | kubectl apply -n ${NAMESPACE} -f -

# Wait for rollout
kubectl rollout status deployment/sre-app -n ${NAMESPACE} --timeout=120s

echo ""
echo "✓ Deploy complete"
