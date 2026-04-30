# Outputs display useful information after terraform apply
# Other Terraform configs or scripts can read these

output "container_name" {
  description = "Name of the running container"
  value       = docker_container.web.name
}

output "container_id" {
  description = "ID of the running container"
  value       = docker_container.web.id
}

output "app_url" {
  description = "URL to access the application"
  value       = "http://localhost:${var.external_port}"
}
