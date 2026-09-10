# Week 17 — Troubleshooting Challenges
 
Diagnosing broken workloads cold — no walkthrough, walk the chain: get -> describe -> logs -> events.

## Challenge 1 — ImagePullBackOff
Symptom: pods stuck ImagePullBackOff.
Diagnosis: describe pod -> Events showed image "nginx:1.29-alpin" not found on registry (typo).
Root cause: misspelled image tag (should be nginx:1.29-alpine).
Fix: kubectl edit deployment / kubectl set image to correct the tag. Pods rolled out clean.

## Challenge 2 — ContainerCreating (stuck)
Symptom: pod stuck ContainerCreating.
Diagnosis: describe pod -> Events "configmap app-settings not found". Logs empty because container never started.
Root cause: pod mounts a ConfigMap that does not exist.
Fix: created the missing ConfigMap. Kubelet retried the mount automatically, pod started.
Lesson: for mount/config failures, logs are useless (container never ran) — describe/Events is the source of truth.

## Challenge 3 — Service with no endpoints
Symptom: pods healthy and Running, but service unreachable ("connection refused").
Diagnosis: kubectl get endpoints -> <none>. Service selector (app: challenge-3-web) did not match pod labels (app: challenge-3).
Root cause: selector/label mismatch.
Fix: corrected the service selector. Endpoints populated with both pod IPs, curl returned nginx page.
Lesson: this failure shows NO error in describe/logs — get endpoints is the definitive check.

## Diagnostic commands
- kubectl get pods -n <ns>
- kubectl describe pod <name> -n <ns>   (read the Events section)
- kubectl logs <pod> -n <ns> [--previous]
- kubectl get endpoints <svc> -n <ns>
- kubectl run testcurl --image=busybox:1.36 -n <ns> --rm -it --restart=Never -- wget -qO- <svc>

## Challenge 4 — Pending pod (storage, not scheduling)
Symptom: pod stuck Pending. describe pod Events said "FailedScheduling: unbound PersistentVolumeClaims" — looks like scheduling, but the real cause is storage.
Diagnosis: dropped a layer — kubectl get pvc showed the PVC also Pending. describe pvc Events: storageclass "fast-ssd" not found. get storageclass confirmed only "standard" exists.
Root cause: PVC referenced a StorageClass that does not exist, so it never bound; pod cannot schedule without its volume.
Fix: storageClassName is immutable, so deleted the pod, deleted the PVC, recreated both against the real "standard" class. PVC bound (WaitForFirstConsumer binds once the pod consumes it), pod Running.
Lesson: a "FailedScheduling" message can be a storage problem in disguise — read the actual Events text, do not trust the label. When a pod is Pending, ask: scheduling or storage?

## Diagnostic commands (storage)
- kubectl get pvc -n <ns>
- kubectl describe pvc <name> -n <ns>   (Events = why it will not bind)
- kubectl get storageclass
