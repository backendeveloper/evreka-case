terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 2.0"
    }
  }
}

# provider "docker" {
#   host = "unix:///var/run/docker.sock"
# }

provider "docker" {
  host = "unix:///Users/kaanuygur/.docker/run/docker.sock"
}

