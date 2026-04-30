# Tell Terraform which providers to use
# Providers are plugins that know how to talk to specific APIs

terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"    # Docker provider from the Terraform registry
      version = "~> 3.0"                # Any 3.x version
    }
  }
}

# Configure the Docker provider
# Connects to Docker via the Unix socket (same socket dockerd listens on)
provider "docker" {
  host = "unix:///var/run/docker.sock"
}
