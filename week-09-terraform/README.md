# Week 9 — Terraform Fundamentals

## What I Built
- Managed Docker containers entirely through Terraform code
- Demonstrated the full lifecycle: init, plan, apply, modify, destroy, recreate
- Used variables for reusable config and outputs for extracting info
- Proved infrastructure can be created and destroyed from the same code files

## Terraform Lifecycle
1. terraform init — download provider plugins
2. terraform plan — preview changes (dry run)
3. terraform apply — execute changes
4. terraform destroy — remove everything

## Key Concepts Learned
- **HCL**: HashiCorp Configuration Language (Terraform's syntax, not YAML)
- **Providers**: plugins that talk to APIs (Docker, AWS, K8s, etc.)
- **Resources**: things Terraform creates and manages
- **State (terraform.tfstate)**: Terraform's memory of what it created — never delete, never commit to Git
- **Variables**: make configs reusable, override via CLI or .tfvars files
- **Outputs**: extract info after apply (URLs, IDs, names)
- **Plan before apply**: always preview changes — your safety net
- **Dependency graph**: Terraform infers order from references (image before container)
- **Destroy**: one command removes everything — Ansible can't do this easily
- **Terraform vs Ansible**: Terraform provisions (creates infrastructure), Ansible configures (sets up software)

## The Lifecycle in Action
- Created nginx container on port 8888
- Modified port to 9999 — Terraform destroyed old, created new automatically
- Planned port 7777 via CLI variable — no file edit needed
- Destroyed everything — container gone, port closed
- Recreated from same code — identical result in 1 second

## Files
- providers.tf — Docker provider configuration
- main.tf — resource definitions (image + container)
- variables.tf — input variables with types and defaults
- outputs.tf — extracted values displayed after apply
- terraform.tfvars — variable values
- .gitignore — excludes state files and provider cache
