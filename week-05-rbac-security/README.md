# Week 5 — RBAC & Security

## What I Built
- Two namespaces (team-alpha, team-beta) simulating team isolation
- Two Roles: pod-reader (read-only) and developer (read/write)
- Two ServiceAccounts (alice, bob) with different permission levels
- Security comparison: insecure (root) vs secure (non-root, read-only fs) containers
- Python Kubernetes client that authenticates using ServiceAccount tokens

## Key Concepts Learned
- **RBAC is default-deny**: no permissions unless explicitly granted
- **Role**: permissions scoped to one namespace
- **RoleBinding**: connects a ServiceAccount to a Role
- **ServiceAccount**: identity for processes in pods
- **kubectl auth can-i**: test permissions without running commands
- **--as flag**: impersonate a user/SA to verify access
- **SecurityContext**: run as non-root, read-only filesystem, drop capabilities
- **readOnlyRootFilesystem**: prevents attackers from writing files in the container
- **Kubernetes Python client**: programmatic API access using SA tokens
- **Namespace isolation**: Roles in one namespace don't grant access to another

## Files
- role-readonly.yaml — pod-reader Role (get, list, watch)
- role-developer.yaml — developer Role (full CRUD on pods, services, deployments)
- serviceaccounts.yaml — alice and bob ServiceAccounts
- rolebindings.yaml — alice gets pod-reader, bob gets developer
- security-demo.yaml — insecure vs secure container deployments
- k8s_client.py — Python script using Kubernetes API
- Dockerfile — container for the Python client
- requirements.txt — kubernetes Python package
