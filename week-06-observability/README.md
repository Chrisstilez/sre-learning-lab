# Week 6 — Troubleshooting & Observability

## What I Built
- Installed Helm (Kubernetes package manager)
- Deployed full Prometheus + Grafana monitoring stack via Helm
- Built a Python Flask app with custom Prometheus metrics (Counter, Histogram, Gauge)
- Generated traffic and observed metrics in Prometheus format
- Deliberately broke deployments and debugged them
- Troubleshot Kind containerd content store corruption

## Key Concepts Learned
- **Helm**: one command installs complex multi-component applications
- **Prometheus**: scrapes /metrics endpoints, stores time series data
- **Grafana**: visualises metrics in dashboards, pre-built K8s dashboards included
- **Metric types**: Counter (only up), Gauge (up/down), Histogram (distribution)
- **prometheus_client**: Python library to expose custom metrics
- **Annotations**: prometheus.io/scrape tells Prometheus which pods to monitor
- **Rolling updates**: bad image only affects new pod, healthy pods keep running
- **ErrImageNeverPull**: image not local + imagePullPolicy Never
- **Rollback**: kubectl rollout undo instantly reverts to previous version
- **Production Grafana**: accessed via Ingress with TLS + SSO, not port-forward

## Monitoring Stack Components
- Prometheus — metrics collection and storage
- Grafana — dashboards and visualisation
- Alertmanager — alert routing and notifications
- node-exporter (x3) — hardware/OS metrics per node
- kube-state-metrics — Kubernetes object metrics
- prometheus-operator — manages Prometheus via K8s resources

## Troubleshooting Session
- Kind containerd content store corrupted after 3 weeks of image loads
- Debugging steps: checked disk (df -h), checked containerd (crictl info), compared images across nodes (crictl images), found duplicate/corrupted entries, cleaned stale images (crictl rmi), restarted containerd
- Pragmatic decision: schedule cluster rebuild at Phase 2 start rather than disrupt working workloads now

## Deliberate Break Scenarios
- Deployed nonexistent image — ErrImageNeverPull, rolling update protected healthy pods
- Rollback with kubectl rollout undo — instant recovery
- Kubernetes never kills healthy pods until replacement is ready

## Files
- metrics-app.py — Flask app with Prometheus metrics
- metrics-deployment.yaml — K8s deployment with Prometheus scrape annotations
- Dockerfile — container build
- requirements.txt — flask + prometheus_client
