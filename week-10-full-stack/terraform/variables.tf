variable "cluster_name" {
  description = "Name of the Kind cluster"
  type	      = string
  default     = "sre-dojo"
}

variable "worker_count" {
  description = "Number of worker nodes"
  type        = number
  default     = 2
}
