# Week 2 — ConfigMaps, Secrets & Environment Management

## What I Built
- Python Flask app that reads all config from environment variables and files
- Deployed to Kubernetes with ConfigMaps and Secrets
- Demonstrated hot reload via mounted ConfigMap

## Key Concepts Learned
- **ConfigMap**: stores non-sensitive config as key-value pairs
- **Secret**: stores sensitive data (base64 encoded, NOT encrypted)
- **envFrom**: injects all keys as environment variables (set at startup, need restart to change)
- **volumeMount**: mounts ConfigMap as files (auto-updates within ~60 seconds)
- **stringData vs data**: stringData accepts plain text, data requires base64
- Twelve-factor app: separate config from code, same image across environments

## Files
- `app.py` — Flask app with /, /secret, /features, /health endpoints
- `Dockerfile` — Python slim-based container
- `requirements.txt` — Python dependencies
- `configmap.yaml` — app configuration (APP_ENV, LOG_LEVEL, etc.)
- `configmap-file.yaml` — feature flags as mounted JSON file
- `secret.yaml` — database credentials
- `deployment.yaml` — K8s deployment with ConfigMap + Secret + volume mount
