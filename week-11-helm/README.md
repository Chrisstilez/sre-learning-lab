# Week 11 — Helm Package Manager

## What I Built
Created a Helm chart from scratch, deployed the same application across multiple environments with different configurations, and tested the full upgrade/rollback lifecycle.

## Chart Structure

web-app/
  Chart.yaml              — Chart identity (name, version, appVersion)
  values.yaml             — Default configuration
  values-dev.yaml         — Dev overrides (1 replica, minimal resources)
  values-prod.yaml        — Prod overrides (5 replicas, higher limits)
  templates/
    deployment.yaml       — Deployment with Go template placeholders
    service.yaml          — Service with conditional nodePort
    _helpers.tpl          — Reusable template functions (names, labels)
    NOTES.txt             — Post-install message
    tests/
      test-connection.yaml

## Key Concepts Demonstrated

### Template Rendering
- Go template syntax: .Values.replicaCount, include, with
- _helpers.tpl for consistent naming (release-name + chart-name, truncated to 63 chars)
- Conditional blocks: nodePort only renders when service type is NodePort
- toYaml | nindent for safe YAML indentation
- Image tag fallback: .Values.image.tag | default .Chart.AppVersion

### Multi-Environment Deployment
Same chart deployed to dev and prod with different values files:
- Dev: 1 replica, ClusterIP, 25m CPU / 32Mi memory
- Prod: 5 replicas, NodePort, 100m CPU / 128Mi memory
- Command: helm install web-prod ./web-app -n prod -f web-app/values-prod.yaml

### Values Override Priority
1. --set flags (highest)
2. -f values-prod.yaml
3. values.yaml in chart (lowest — defaults)

### Upgrade and Rollback

| Rev | Action | Result |
|-----|--------|--------|
| 1 | Install nginx:1.27-alpine | Success |
| 2 | Upgrade to nginx:1.28-alpine | Success |
| 3 | Upgrade to nginx:doesnt-exist | Failed — ImagePullBackOff |
| 4 | Rollback to revision 2 | Success — 1.28-alpine restored |

Kubernetes rolling update protection: failed upgrade left old pods running. Rollback with one command: helm rollback web-prod 2 -n prod

### helm template
Renders all templates locally without installing — the Helm equivalent of terraform plan. Used to verify image tags, replica counts, and YAML structure before applying to the cluster.

## Connection to Grafana Upgrade Lab
The Grafana upgrade used the same Helm patterns tested here:
- helm upgrade with --reuse-values and --set image.tag
- helm rollback when 13.0.0 tag didn't exist
- helm history to track all revisions
- Same chart version, different image tag (chart packaging vs app version)
