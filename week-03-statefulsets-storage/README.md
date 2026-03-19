# Week 3 — Persistent Storage & StatefulSets

## What I Built
- Proved containers are ephemeral (data lost on deletion)
- Proved Docker volumes survive container deletion
- Deployed PostgreSQL using a StatefulSet with persistent storage in Kubernetes
- Built a Python CLI tool that connects to PostgreSQL and manages data
- Demonstrated data surviving pod deletion

## Key Concepts Learned
- **PersistentVolume (PV)**: actual storage provisioned in the cluster
- **PersistentVolumeClaim (PVC)**: a request for storage — binds to a PV
- **StorageClass**: auto-provisions PVs when PVCs are created (dynamic provisioning)
- **WaitForFirstConsumer**: PV not created until a pod needs it (provisions on correct node)
- **StatefulSet vs Deployment**: StatefulSet gives ordered pod names (postgres-0), stable DNS, and per-pod PVCs
- **Headless Service (clusterIP: None)**: creates per-pod DNS records instead of load balancing
- **volumeClaimTemplates**: each StatefulSet replica gets its own PVC automatically
- **Data survives pod deletion**: PVC persists independently, new pod remounts it

## Files
- `pvc.yaml` — standalone PVC test
- `test-pod.yaml` — pod with mounted PVC
- `postgres-secret.yaml` — database credentials
- `postgres-statefulset.yaml` — PostgreSQL StatefulSet + headless Service
- `db_client.py` — Python CLI for database operations
- `Dockerfile` — container for the Python client
- `requirements.txt` — Python dependencies

## Debugging Note
CoreDNS stopped syncing with the API server after cluster restarts. Fix: `kubectl rollout restart deployment coredns -n kube-system`
