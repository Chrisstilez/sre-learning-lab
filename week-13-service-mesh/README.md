# Week 13 — Service Mesh (Linkerd)

## What I Built
Deployed a two-service microservice application (frontend calling backend) through a Linkerd service mesh, demonstrating automatic mTLS encryption, traffic observability, and canary deployments via traffic splitting.

## Architecture

  Browser → Frontend (port 30090) → Backend (port 8080) → JSON response
                |                        |
           [proxy sidecar]          [proxy sidecar]
                |                        |
           Linkerd Control Plane (identity, destination, proxy-injector)

## What Linkerd Added (Zero Code Changes)

### Automatic mTLS
Every pod-to-pod request encrypted and authenticated. Confirmed via linkerd viz tap showing tls=true on all requests. No certificates configured manually — Linkerd identity service manages rotation automatically.

### Traffic Observability
linkerd viz stat shows per-deployment success rate, RPS, and latency percentiles (P50/P95/P99) — all collected by the proxy sidecars without any instrumentation code.

### Canary Deployment via Traffic Splitting
Deployed backend-v2 alongside backend-v1 and shifted traffic gradually:

| Split | v1 Requests | v2 Requests | Action |
|-------|-------------|-------------|--------|
| 90/10 | 19 | 1 | Canary — minimal exposure |
| 50/50 | 10 | 10 | Gaining confidence |
| 0/100 | 0 | 20 | Full rollout to v2 |

Used Linkerd HTTPRoute (policy.linkerd.io/v1beta3) with weighted backendRefs. Changed weights, applied, traffic shifted instantly. No downtime, no code changes.

## Key Concepts Demonstrated

### Sidecar Injection
Namespace annotation linkerd.io/inject=enabled causes the proxy-injector webhook to automatically add a sidecar container to every pod. Pods show 2/2 READY (app + proxy).

### Control Plane vs Data Plane
- Control plane: linkerd-identity (certs), linkerd-destination (routing), linkerd-proxy-injector (webhook)
- Data plane: proxy sidecars in every meshed pod handling actual traffic

### Observability Without Instrumentation
linkerd viz stat, linkerd viz edges, and linkerd viz tap provided full request-level visibility without adding any logging, metrics, or tracing libraries to the application code.

## Project Structure

  apps/
    backend.py          — Backend service (/api/data, /health)
    frontend.py         — Frontend service (calls backend, /health)
    Dockerfile          — Shared Dockerfile with APP_FILE build arg
  k8s/
    namespace.yaml      — mesh-demo namespace with Linkerd injection annotation
    backend.yaml        — Backend v1 Deployment + Service
    backend-v2.yaml     — Backend v2 Deployment (canary)
    backend-services.yaml — Separate Services for v1 and v2 (for traffic splitting)
    frontend.yaml       — Frontend Deployment + NodePort Service
    traffic-split.yaml  — HTTPRoute with weighted backends

## Tools Used
- Linkerd (edge-26.6.1) with Viz extension
- Gateway API HTTPRoute for traffic splitting
- Docker Hub for images (christopher95/mesh-backend, mesh-frontend)
