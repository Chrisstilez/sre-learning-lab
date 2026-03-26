# Week 4 — Networking Deep Dive

## What I Built
- Frontend (Flask) and Backend (Flask API) as separate microservices
- Deployed both to Kubernetes with Services (ClusterIP + NodePort)
- Installed NGINX Ingress Controller for path-based routing
- Applied NetworkPolicy to restrict backend access to frontend only

## Key Concepts Learned
- **Microservices**: small focused apps that communicate over the network
- **ClusterIP Service**: internal-only stable endpoint, used for backend
- **NodePort Service**: externally accessible, used for frontend
- **Service load balancing**: requests spread across pods automatically
- **Service discovery**: frontend calls backend by Service name (CoreDNS resolves it)
- **Ingress**: L7 routing — one entry point, routes by URL path (/ → frontend, /api → backend)
- **Ingress Controller**: NGINX processes the Ingress rules and routes traffic
- **Host header**: tells the Ingress controller which rule set to use
- **NetworkPolicy**: Kubernetes firewall — backend only accepts traffic from frontend pods
- **Default-deny**: once a NetworkPolicy selects a pod, all unspecified traffic is blocked

## Architecture
Browser → Ingress (/  → frontend Service → frontend pods)
                  (/api → backend Service → backend pods)
NetworkPolicy: only frontend pods can reach backend on port 8080

## Files
- backend.py — Flask API returning JSON
- frontend.py — Flask web app calling backend
- Dockerfile.backend / Dockerfile.frontend — container builds
- requirements.txt — Python dependencies (flask, requests)
- deployments.yaml — both Deployments and Services
- ingress.yaml — path-based routing rules
- network-policy.yaml — backend firewall
