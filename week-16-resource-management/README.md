# Week 16 — Resource Management & Autoscaling

## What I Built
Explored how Kubernetes manages and protects resources across multi-tenant workloads: quotas, priority-based preemption, disruption budgets, and horizontal autoscaling.

## Part 1: ResourceQuota + LimitRange

Set up a namespace (team-alpha) with both controls:
- LimitRange: per-container defaults (100m/128Mi request, 200m/256Mi limit), max 1 CPU / 1Gi, min 50m / 64Mi
- ResourceQuota: namespace total 2 CPU / 2Gi requests, 4 CPU / 4Gi limits, 10 pods max

Key observations:
- Deployed a pod with NO resource spec — LimitRange auto-injected the defaults
- Tried to exceed the max — rejected with "must be less than or equal to cpu limit"
- Scaled a deployment to 25 replicas — quota capped it at 10 pods (pods limit hit before CPU limit)
- Quota describe showed exact usage: pods 10/10, requests.cpu 1/2, limits.cpu 2/4

Lesson: quota enforces ALL limits simultaneously; whichever is hit first blocks new pods.

## Part 2: PriorityClasses + Preemption

Created two priority classes (low=100, high=1000000). Filled a node with 3 low-priority pods (6 CPU / 6Gi), then deployed a high-priority pod needing 2 CPU / 2Gi.

Result: scheduler evicted a low-priority pod to make room for the high-priority pod. The Deployment tried to recreate the evicted pod but it stayed Pending — no room left, and it can't evict the high-priority pod.

This is how critical workloads guarantee scheduling on a full cluster.

## Part 3: PodDisruptionBudget

Deployed 4 web pods, set a PDB with minAvailable=3 (allowed disruptions = 1). Drained a node holding 2 of them.

The drain output showed the PDB enforcing the budget:
- First pod evicted (dropped to 3, still meets minimum)
- Second pod eviction BLOCKED: "Cannot evict pod as it would violate the pod's disruption budget"
- Waited for the first pod's replacement to be Running
- Then evicted the second pod

Never dropped below 3 running pods during the entire drain. This protects services during rolling maintenance.

## Part 4: Horizontal Pod Autoscaler

Installed metrics-server (with --kubelet-insecure-tls for Kind). Deployed the hpa-example PHP app with a 100m CPU request. Created an HPA targeting 50% CPU, min 1, max 10.

Generated load with an infinite wget loop. Watched HPA scale:
- Idle: cpu 1%, 1 replica
- Load hit: cpu 174%, still 1 replica
- HPA scaled: 1 × (174/50) = 3.48 → 4 replicas
- Load spread across 4 pods: cpu dropped to 41%

Confirmed the core concept: more pods distribute the same load, reducing per-pod CPU. Scale-down uses a 5-minute stabilization window to prevent flapping.

## Key Concepts
- Requests are reservations (scheduler uses these); limits are hard caps (throttle/OOMKill)
- HPA calculates against requests, not limits: utilisation = actual / request
- LimitRange = per-container guardrails; ResourceQuota = namespace-wide budget
- PriorityClass enables preemption — high-priority pods evict low-priority ones when full
- PDB guarantees minimum availability during voluntary disruptions (drain, rolling updates)
- HPA formula: desiredReplicas = currentReplicas × (currentMetric / targetMetric)
