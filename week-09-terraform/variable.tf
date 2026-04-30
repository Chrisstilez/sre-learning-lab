# Variables make your Terraform reusable
# Change values here or override at runtime — code stays the same

variable "container_name" {
  description = "Name for the web container"
  type        = string
  default     = "terraform-web"
}

variable "external_port" {
  description = "Port exposed on the host"
  type        = number
  default     = 9999
}

variable "internal_port" {
  description = "Port inside the container"
  type        = number
  default     = 80
}

variable "image_name" {
  description = "Docker image to use"
  type        = string
  default     = "nginx:alpine"
}
