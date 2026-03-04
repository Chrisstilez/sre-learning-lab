# Week 1 — Multi-Node Cluster & Pod Scheduling

## What I Built
- 3-node Kind cluster (1 control plane + 2 workers)
- Tested 5 scheduling scenarios

## Key Concepts Learned
- Scheduler filters nodes then scores them to pick the best fit
- **nodeSelector**: hard requirement — pod only runs on nodes with matching label
- **Node labels**: key-value tags on nodes (disk=ssd, gpu=true)
- **Taints & Tolerations**: nodes reject pods unless they have a matching toleration
  - NoSchedule: blocks new pods, existing stay
  - NoExecute: evicts existing pods too
- **Pod Anti-Affinity**: spread replicas across nodes for high availability
- Control plane taint prevents workload pods from scheduling there

## Files
- `kind-config.yaml` — 3-node cluster definition
- `deploy-basic.yaml` — basic deployment (scheduler spreads across workers)
- `deploy-ssd-only.yaml` — nodeSelector example (all pods on SSD node)
- `deploy-gpu.yaml` — unmatched label (pods stay Pending)
- `deploy-spread.yaml` — pod anti-affinity (1 pod per node)

## Commands Reference
```bash
kubectl label node <name> key=value          # add label
kubectl taint node <name> key=value:effect   # add taint
kubectl taint node <name> key=value:effect-  # remove taint (note the -)
kubectl get pods -o wide                     # see which node pods land on
kubectl describe pod <name>                  # Events section shows WHY
kubectl get nodes --show-labels              # see all labels
```
