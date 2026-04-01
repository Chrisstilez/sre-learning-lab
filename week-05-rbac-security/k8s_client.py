# Kubernetes Python client — demonstrates programmatic cluster access
# This script runs inside a pod and uses the pod's ServiceAccount token
# to authenticate with the Kubernetes API

from kubernetes import client, config  # Official K8s Python library
import sys

def connect():
    """Connect to Kubernetes API using the pod's ServiceAccount token"""
    try:
        config.load_incluster_config()  # Auto-loads token from /var/run/secrets/
        return True
    except:
        print("Not running inside a cluster. Trying local kubeconfig...")
        try:
            config.load_kube_config()   # Falls back to ~/.kube/config
            return True
        except:
            print("Cannot connect to Kubernetes.")
            return False

def list_pods(namespace):
    """List all pods in a namespace — requires 'get' and 'list' verbs on pods"""
    v1 = client.CoreV1Api()                              # Core API (pods, services, etc.)
    pods = v1.list_namespaced_pod(namespace=namespace)    # API call to list pods
    print(f"\nPods in namespace '{namespace}':")
    print(f"{'NAME':<45} {'STATUS':<12} {'IP':<16} {'NODE'}")
    print("-" * 90)
    for pod in pods.items:
        name = pod.metadata.name
        status = pod.status.phase                        # Running, Pending, etc.
        ip = pod.status.pod_ip or "N/A"
        node = pod.spec.node_name or "N/A"
        print(f"{name:<45} {status:<12} {ip:<16} {node}")
    print(f"\nTotal: {len(pods.items)} pods")

def list_services(namespace):
    """List all services in a namespace"""
    v1 = client.CoreV1Api()
    services = v1.list_namespaced_service(namespace=namespace)
    print(f"\nServices in namespace '{namespace}':")
    print(f"{'NAME':<30} {'TYPE':<15} {'CLUSTER-IP':<18} {'PORTS'}")
    print("-" * 80)
    for svc in services.items:
        name = svc.metadata.name
        svc_type = svc.spec.type
        cluster_ip = svc.spec.cluster_ip or "None"
        ports = ", ".join([f"{p.port}/{p.protocol}" for p in svc.spec.ports]) if svc.spec.ports else "N/A"
        print(f"{name:<30} {svc_type:<15} {cluster_ip:<18} {ports}")

def count_all(namespace):
    """Quick summary of resources in a namespace"""
    v1 = client.CoreV1Api()
    apps_v1 = client.AppsV1Api()                         # Apps API (deployments)
    pods = v1.list_namespaced_pod(namespace=namespace)
    services = v1.list_namespaced_service(namespace=namespace)
    deployments = apps_v1.list_namespaced_deployment(namespace=namespace)
    print(f"\nResource summary for namespace '{namespace}':")
    print(f"  Pods:        {len(pods.items)}")
    print(f"  Services:    {len(services.items)}")
    print(f"  Deployments: {len(deployments.items)}")

if __name__ == "__main__":
    if not connect():
        sys.exit(1)

    if len(sys.argv) < 3:
        print("Usage:")
        print("  python k8s_client.py pods <namespace>")
        print("  python k8s_client.py services <namespace>")
        print("  python k8s_client.py summary <namespace>")
        sys.exit(0)

    command = sys.argv[1]       # What to do (pods, services, summary)
    namespace = sys.argv[2]     # Which namespace to look at

    if command == "pods":
        list_pods(namespace)
    elif command == "services":
        list_services(namespace)
    elif command == "summary":
        count_all(namespace)
    else:
        print(f"Unknown command: {command}")
