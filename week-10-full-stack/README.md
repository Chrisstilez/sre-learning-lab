# Week 10 — Full Stack: Terraform + Ansible + Kubernetes

## What I Built
- Complete IaC project with separation of concerns across three tools
- One command (make all) creates a Kubernetes cluster and deploys everything on top
- One command (make destroy) tears it all down
- One command (make status) shows the full picture

## Separation of Concerns
- **Terraform** provisions infrastructure (Kind cluster via Docker)
- **Ansible** configures and deploys (namespaces, apps, monitoring)
- **Kubernetes manifests** define application state (Deployments, Services)
- **Makefile** orchestrates the workflow

## Project Structure
Makefile (orchestrator)
├── terraform/ (infrastructure)
│   ├── providers.tf — Kind provider
│   ├── variables.tf — cluster name, worker count
│   ├── main.tf — cluster resource with dynamic worker nodes
│   └── outputs.tf — cluster name, endpoint, kubeconfig
├── ansible/ (configuration)
│   ├── playbook.yml — master playbook
│   ├── inventory.ini — localhost
│   ├── vars/main.yml — app and monitoring config
│   ├── secrets.yml — vault-encrypted Grafana password
│   └── roles/
│       ├── cluster-setup/ — verify cluster, create namespaces
│       ├── apps/ — apply K8s manifests from k8s/ directory
│       └── monitoring/ — Prometheus + Grafana via Helm
├── k8s/ (application state)
│   ├── deployments/web-app.yaml — nginx with resource limits
│   └── services/web-app.yaml — NodePort service
└── .gitignore — excludes tfstate, vault password, provider cache

## Key Concepts Learned
- **Separation of concerns**: each tool handles one layer, not everything
- **Makefile orchestration**: single entry point, individual targets for each phase
- **Terraform dynamic blocks**: loop-generated worker nodes from a variable
- **Ansible src parameter**: point to external K8s manifests instead of embedding YAML
- **Vault password file**: .vault_pass enables non-interactive automation
- **Resource requests/limits**: set on all pods so percentage-based monitoring works
- **.gitignore**: code in Git, secrets and state files never

## Makefile Targets
- make all — full build: infrastructure + configuration
- make infra — Terraform only (create cluster)
- make configure — Ansible only (deploy apps + monitoring)
- make deploy — apps only
- make monitor — monitoring only
- make status — show cluster, pods, services
- make destroy — tear everything down

## Full Lifecycle Demonstrated
1. make all — built cluster + deployed 3 app pods + full monitoring stack
2. make status — verified everything running
3. make destroy — removed everything in 2 seconds
4. make all — rebuilt identical environment from scratch
