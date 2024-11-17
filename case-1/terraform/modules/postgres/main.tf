resource "docker_volume" "postgres_data" {
  name = "postgres_data"
}

resource "docker_image" "postgres_image" {
  name = "postgres:17.1"
}

resource "docker_container" "postgres" {
  name  = "postgres-db"
  image = docker_image.postgres_image.image_id

  ports {
    internal = 5432
    external = 5432
  }

  env = [
    "POSTGRES_USER=postgres",
    "POSTGRES_PASSWORD=postgres",
    "POSTGRES_DB=evreka-db"
  ]

  volumes {
    volume_name    = docker_volume.postgres_data.name
    container_path = "/var/lib/postgresql/data"
  }

  healthcheck {
    test = ["CMD-SHELL", "pg_isready -U postgres"]
    interval = "10s"
    timeout  = "5s"
    retries  = 5
  }

  networks_advanced {
    name = var.network_name
    aliases = ["postgres"]
  }

  restart = "always"
}