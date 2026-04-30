# Pull the Docker image
resource "docker_image" "nginx" {
  name         = var.image_name       # From variables.tf
  keep_locally = true
}

# Create a container
resource "docker_container" "web" {
  name  = var.container_name          # From variables.tf
  image = docker_image.nginx.image_id

  ports {
    internal = var.internal_port      # From variables.tf
    external = var.external_port      # From variables.tf
  }
}
