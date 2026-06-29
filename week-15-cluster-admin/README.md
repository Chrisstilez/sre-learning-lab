# Week 15 — Cluster Administration

## What I Explored
Investigated Kubernetes cluster internals — control plane components, static pods, etcd backup, and node maintenance with drain/uncordon.

## Control Plane Components

Examined every component running in kube-system:

| Component | Type | Role |
|-----------|------|------|
| etcd | Static Pod (Owner: Node) | Cluster state database |
| kube-apiserver | Static Pod (Owner: Node) | API front door for all requests |
| kube-scheduler | Static Pod (Owner: Node) | Assigns pods to nodes |
| kube-controller-manager | Static Pod (Owner: Node) | Runs reconciliation loops |
| coredns | ReplicaSet | Cluster DNS resolution |
| kube-proxy | DaemonSet (every node) | Service networking rules |
| kindnet | DaemonSet (every node) | CNI — pod-to-pod networking |

Static pods are defined in /etc/kubernetes/manifests/ on the control plane node. The kubelet runs them directly — no scheduler involved (chicken-and-egg: you can't schedule the scheduler).

## Static Pods vs Regular Pods
- Static pods: Owner is Node, name includes node name (etcd-sre-dojo-control-plane)
- ReplicaSet pods: Owner is ReplicaSet, name has random suffix (coredns-7d764666f9-79n86)
- DaemonSet pods: Owner is DaemonSet, one per node (kube-proxy on all 3 nodes)

## etcd Backup
Performed etcd snapshot backup using etcdctl inside the etcd pod:
- Connected with TLS certificates from /etc/kubernetes/pki/etcd/
- Created 20MB snapshot of all cluster state
- Pattern: etcdctl snapshot save with --endpoints, --cacert, --cert, --key

## Node Drain and Uncordon
Simulated node maintenance on worker2:

1. Deployed 4 nginx pods across both workers (2 on each)
2. Ran kubectl drain sre-dojo-worker2 --ignore-daemonsets --delete-emptydir-data
3. Result: node cordoned (SchedulingDisabled), all non-DaemonSet pods evicted
4. All 4 test pods moved to worker (scheduler rescheduled automatically)
5. DaemonSet pods (kube-proxy, kindnet, promtail) stayed — they belong on every node
6. kubectl uncordon brought the node back to Ready

Cordon vs Drain:
- cordon: stop new pods, keep existing ones running
- drain: cordon + evict everything — node is empty and safe to take offline

## Key Concepts
- etcd is the single source of truth — if lost without backup, cluster state is gone
- Static pods solve the bootstrap problem — control plane runs before the scheduler exists
- Drain is graceful — pods get their termination grace period before eviction
- DaemonSets are immune to drain because they must run on every node
- Kubernetes does not auto-rebalance after uncordon — new pods consider the node, existing ones stay
