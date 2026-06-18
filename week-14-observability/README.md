# Week 14 — Full Observability Stack

## What I Built
Added the remaining observability pillars to the Kubernetes cluster: centralised logging with Loki/Promtail and alerting with Prometheus rules. Combined with the existing Prometheus/Grafana metrics from earlier weeks, this completes the three pillars of observability.

## Three Pillars Demonstrated

### 1. Metrics (Prometheus + Grafana)
Already in place from Week 6/10. Numerical time-series data — CPU, memory, request rates, error rates. Answers "what is happening right now" and "how has it changed over time."

### 2. Logs (Loki + Promtail)
Deployed Loki for central log storage and Promtail as a DaemonSet (one agent per node) to ship container logs.

Queried logs using LogQL:
- {namespace="monitoring"} — all logs from a namespace
- {app="logger-app"} |= "ERROR" — filter for error lines across all pods

Key result: searched across two pods and found all "Database connection timeout" errors in one query, instead of running kubectl logs on each pod individually.

### 3. Alerting (Prometheus Alert Rules)
Created 5 custom alert rules across 3 groups:

| Alert | Severity | Condition |
|-------|----------|-----------|
| PodCrashLooping | critical | Pod restart rate > 0 for 2 minutes |
| PodNotReady | warning | Pod not ready for 5 minutes |
| NodeHighMemory | warning | Node memory > 85% for 5 minutes |
| NodeHighCPU | warning | Node CPU > 85% for 5 minutes |
| NodeNotReady | critical | Node not ready for 2 minutes |

All 5 rules verified as inactive (cluster healthy). Rules use the PrometheusRule CRD which the kube-prometheus-stack operator picks up automatically.

## Log-Generating Test App
Deployed a Python app that simulates a flaky service — 30% of requests return "Database connection timeout after 30s" errors. Used to demonstrate LogQL filtering and prove Loki collects logs from all pods.

## Project Structure

  loki/
    values-loki.yaml        — Loki-stack Helm values
    values-promtail.yaml    — Promtail configuration
  alerts/
    alert-rules.yaml        — PrometheusRule with 5 alert definitions
  app/
    logger-app.py           — Flaky app that generates errors for log testing
    Dockerfile.logger       — Dockerfile for the logger app
  k8s/
    logger-app.yaml         — Deployment + Service for the logger app

## Key Concepts

### LogQL
Loki's query language. Label selectors ({app="logger-app"}) choose which streams to search. Pipe operators (|= "ERROR") filter log content. Like PromQL for metrics but for logs.

### Promtail DaemonSet
One Promtail pod per node reads container log files from the node filesystem and ships them to Loki. No application changes needed — every container's stdout/stderr is collected automatically.

### Alert on Symptoms Not Causes
Alert rules target user-facing symptoms: pod not ready, node not ready. Not low-level causes like "disk IOPS high" that might not affect users. Every alert should require human action.

### Severity Levels
Critical — immediate action (PodCrashLooping, NodeNotReady). Warning — investigate during business hours (high memory, high CPU, pod not ready).

## Connection to Previous Weeks
- Week 6/10: Prometheus and Grafana already provided metrics
- Week 11: Helm used to deploy Loki stack
- Week 12: The CI/CD app could feed logs to Loki for pipeline debugging
- Week 13: Linkerd provided request-level observability; Loki adds log-level context
