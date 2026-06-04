# Week 12 — CI/CD Pipeline

## What I Built
A four-stage CI/CD pipeline that takes a Python application from code change to running on Kubernetes in one command. The pipeline tests, builds a Docker image, pushes to Docker Hub, and deploys to the cluster — stopping immediately if any stage fails.

## Pipeline Stages

  make pipeline
    |
    v
  TEST -----> FAIL? --> STOP (broken code never reaches cluster)
    |
    v
  BUILD ----> Docker image tagged with git SHA (never "latest")
    |
    v
  PUSH -----> Image pushed to Docker Hub
    |
    v
  DEPLOY ---> sed substitutes image tag into K8s manifest, kubectl apply, rollout wait

## Project Structure

  app/
    app.py              — Python HTTP server (/health, /)
    Dockerfile          — Minimal image (python:3.11-slim)
    tests/
      test_app.py       — 3 unit tests (200 OK, health JSON, 404)
  pipeline/
    test.sh             — Runs unit tests
    build.sh            — Builds Docker image tagged with git SHA
    push.sh             — Pushes to Docker Hub
    deploy.sh           — Substitutes image into manifest, applies, waits for rollout
  k8s/
    deployment.yaml     — Deployment + Service with IMAGE_PLACEHOLDER
  Makefile              — Orchestrates: make pipeline runs all four stages

## Key Concepts Demonstrated

### Git SHA as Image Tag
Every build is tagged with the short git commit SHA (e.g., christopher95/sre-app:0b9d964). No ambiguity about which code is running. Never use "latest" in a pipeline.

### Pipeline Stops on Failure
Deliberately broke the app (changed 200 to 500), ran the pipeline. Tests caught it, pipeline stopped. No build, no push, no deploy. Cluster stayed on the working version.

### Rolling Update
Deploy stage uses kubectl apply which triggers a rolling update. Kubernetes replaces pods one at a time. Combined with readiness probes on /health, traffic only routes to healthy pods.

### Docker Layer Caching
Second build reused all base image layers — only the app layer was rebuilt and pushed. Build went from 25s to 2.6s.

### Two Versions Deployed
- v0.1.0 (git SHA: 194a186) — initial deploy
- v0.2.0 (git SHA: 0b9d964) — code change, full pipeline, verified via /health endpoint

## Connection to Previous Weeks
- Week 10 Makefile orchestration pattern reused here
- Week 11 Helm showed release management — this week shows the build pipeline that feeds into it
- In production, the deploy stage would run helm upgrade instead of kubectl apply
