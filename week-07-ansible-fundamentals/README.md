# Week 7 — Ansible Fundamentals

## What I Built
- Upgraded Ansible from apt version (2.10) to modern version (2.17) via pipx
- First playbook testing idempotency with file/directory/package tasks
- Real playbook that rebuilds a 3-node Kind Kubernetes cluster
- Deployed a full nginx application to Kubernetes using kubernetes.core collection
- Demonstrated scaling by changing variables and re-running the playbook

## Key Concepts Learned
- **Agentless**: Ansible connects via SSH, no software needed on managed nodes
- **Playbook**: YAML file with tasks to execute
- **Task**: single action using a module (apt, copy, file, command, etc.)
- **Idempotent**: running twice = same result, safe to re-run
- **Jinja2 templates**: files with {{ variables }} and {% loops %}
- **register**: capture command output for later use
- **when**: conditional execution based on registered variables
- **changed_when**: control whether a task reports 'changed'
- **become**: run task with sudo
- **kubernetes.core.k8s**: module for managing K8s resources from Ansible
- **until/retries/delay**: wait for a condition before proceeding

## Output States
- **ok**: already in desired state, no changes needed (idempotency working)
- **changed**: had to modify something to reach desired state
- **skipped**: when condition was false, task was not run
- **failed**: something went wrong

## Debugging Note
First playbook used {{ ansible_date_time.iso8601 }} in file content — this broke idempotency
because the timestamp changed every run, causing the task to always report 'changed'. Fixed by
using static content. Lesson: variables that change on every run break idempotency.

## Files
- inventory.ini — host list with localhost
- first-playbook.yml — introductory playbook demonstrating idempotency
- cluster-setup.yml — rebuilds Kind cluster with template-based config
- templates/kind-config.yaml.j2 — Jinja2 template with worker count variable
- deploy-app.yml — deploys nginx Deployment + Service to K8s via Ansible
