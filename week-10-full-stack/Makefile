.PHONY: all infra configure deploy monitor status clean destroy

# Default — runs everything in order
all: infra configure

# Step 1: Terraform creates the cluster
infra:
	@echo "=== Creating infrastructure with Terraform ==="
	cd terraform && terraform init -input=false
	cd terraform && terraform apply -auto-approve

# Step 2: Ansible configures everything on top
configure:
	@echo "=== Configuring with Ansible ==="
	ansible-playbook -i ansible/inventory.ini ansible/playbook.yaml --vault-password-file .vault_pass

# Run only the app deployment
deploy:
	@echo "=== Deploying applications ==="
	ansible-playbook -i ansible/inventory.ini ansible/playbook.yaml --vault-password-file .vault_pass --tags apps

# Run only monitoring setup
monitor:
	@echo "=== Setting up monitoring ==="
	ansible-playbook -i ansible/inventory.ini ansible/playbook.yaml --vault-password-file .vault_pass --tags monitoring

# Show cluster status
status:
	@echo "=== Cluster Status ==="
	@kubectl get nodes
	@echo ""
	@echo "=== Pods ==="
	@kubectl get pods -A | grep -E "production|monitoring"
	@echo ""
	@echo "=== Services ==="
	@kubectl get svc -A | grep -E "NodePort|LoadBalancer"

# Destroy everything
destroy:
	@echo "=== Destroying infrastructure ==="
	cd terraform && terraform destroy -auto-approve
	@echo "=== Infrastructure destroyed ==="
