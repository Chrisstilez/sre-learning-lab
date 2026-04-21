# Week 8 — Ansible + Kubernetes at Scale

## What I Built
- Full role-based Ansible project with 5 roles
- One command deploys: system packages, Docker, Kind cluster, applications, monitoring stack
- Vault-encrypted secrets for database password and Grafana admin password
- Demonstrated idempotency at scale — second run skips everything that exists

## Project Structure
site.yml (master playbook)
  ├── vars/main.yml (plain text config)
  ├── secrets.yml (vault-encrypted passwords)
  └── roles/
      ├── common (apt packages, system info)
      ├── docker (install Docker, skip if exists)
      ├── cluster (Kind + kubectl, skip if cluster exists)
      ├── apps (namespace, Secret from vault, Deployment, Service)
      └── monitoring (Helm, Prometheus, Grafana with vault password)

## Key Concepts Learned
- **Roles**: modular, reusable units of automation
- **Ansible Vault**: AES-256 encryption for secrets, safe to commit to Git
- **Separation of concerns**: each role handles one layer
- **Tags**: run specific roles without running everything
- **kubernetes.core.k8s**: manage K8s resources from Ansible
- **kubernetes.core.helm**: install Helm charts from Ansible
- **get_url module**: download binaries idempotently
- **args: creates**: make shell commands idempotent
- **Production reality**: roles come from Galaxy/company repos, you modify not write from scratch

## Debugging Note
First run failed — cluster_name had an underscore (sre_dojo) which Kind rejects.
Kind only accepts lowercase letters, numbers, dots, and hyphens.
Fixed by changing to sre-dojo in vars/main.yml.

## Files
- site.yml — master playbook connecting all roles
- inventory.ini — localhost target
- vars/main.yml — configuration variables
- secrets.yml — vault-encrypted secrets
- roles/common/tasks/main.yml — base system setup
- roles/docker/tasks/main.yml — Docker installation
- roles/docker/handlers/main.yml — Docker restart handler
- roles/cluster/tasks/main.yml — Kind and kubectl setup
- roles/cluster/templates/kind-config.yaml.j2 — cluster config template
- roles/apps/tasks/main.yml — application deployment
- roles/monitoring/tasks/main.yml — Prometheus and Grafana
