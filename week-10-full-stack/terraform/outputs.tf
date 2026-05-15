output "cluster_name" {
  description = "Name of the created cluster"
  value       = kind_cluster.lab.name
}

output "kubeconfig" {
  description = "Path to kubeconfig"
  value       = kind_cluster.lab.kubeconfig_path
  sensitive   = true
}

output "endpoint" {
  description = "Cluster API endpoint"
  value       = kind_cluster.lab.endpoint
}
