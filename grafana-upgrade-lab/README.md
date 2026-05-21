# Grafana Upgrade Lab — Helm-Based Version Upgrade

## What I Built
Tested a full Grafana upgrade lifecycle on a Kind cluster, covering both
Docker Hub pulls and local image loading, with rollback validation.

## Upgrade Path Tested
- Grafana 12.2.0 → 13.0.0 (failed — tag removed from Docker Hub due to migration bug)
- Rollback to 12.2.0 (helm rollback, restored in seconds)
- Grafana 12.2.0 → 13.0.1 (success — pulled from Docker Hub)
- Grafana 13.0.1 → 13.0.1-security-01 (success — loaded from local image)

## Full Revision History
| Rev | Action | Result |
|-----|--------|--------|
| 1 | Install Grafana 12.2.0 (chart 10.1.2) | Success |
| 2 | Upgrade to 13.0.0 | Failed — tag doesn't exist |
| 3 | Rollback to revision 1 | Success — 12.2.0 restored |
| 4 | Upgrade to 13.0.1 | Success — pulled from Docker Hub |
| 5 | Upgrade to 13.0.1-security-01 (local image) | Success — imagePullPolicy: Never |

## Key Findings
- Tag 13.0.0 was removed from Docker Hub due to a migration bug that caused
  dashboard loss with Git Sync enabled. Always verify tags exist before upgrading.
- Kubernetes rolling update protection works: when the new pod failed to pull
  the image, the old pod kept running. No downtime from a failed upgrade.
- Dashboards were lost during the local image upgrade because persistence was
  disabled (emptyDir volume). In a persistent setup, dashboards survive upgrades.
- The local image workflow uses docker save → pipe into containerd on each node
  via ctr import. imagePullPolicy: Never ensures no external pull attempts.

## Procedures Tested

### Docker Hub Pull

helm upgrade grafana grafana/grafana 
--namespace grafana-upgrade-lab 
--version 10.1.2 
--reuse-values 
--set image.tag=13.0.1

### Local Image Load
docker pull grafana/grafana:13.0.1-security-01
docker save grafana/grafana:13.0.1-security-01 -o /tmp/grafana-13.tar
cat /tmp/grafana-13.tar | docker exec -i <node> ctr --namespace=k8s.io images import -
helm upgrade grafana grafana/grafana 
--namespace grafana-upgrade-lab 
--version 10.1.2 
--reuse-values 
--set image.tag=13.0.1-security-01 
--set image.pullPolicy=Never

### Rollback
helm rollback grafana <revision> -n grafana-upgrade-lab

## Grafana 13 Key Changes
- New: Git Sync (GA), Dashboard Restore, Dashboards API v2, Dynamic Dashboards, Grafana Assistant
- Breaking: Image Renderer plugin removed, /api deprecated for /apis, RBAC tightened, React 19 migration
- Critical: v13.0.0 had migration bug — use v13.0.1 minimum

## Tools Used
- Helm v3.x for release management
- Kind cluster (1 control plane + 2 workers)
- Docker + containerd for local image loading
- Grafana API for dashboard import and health checks

## Deliverable
A formal Method of Procedure (MOP) document was created covering both upgrade
paths with detection steps, pre-checks, execution, verification, and rollback.
