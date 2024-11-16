resource "docker_volume" "rabbitmq_data" {
  name = "rabbitmq_data"
}

resource "docker_image" "rabbitmq_image" {
  name = "rabbitmq:3-management"
}

resource "docker_container" "rabbitmq" {
  name  = "rabbitmq"
  image = docker_image.rabbitmq_image.image_id

  ports {
    internal = 5672
    external = 5672
  }
  ports {
    internal = 15672
    external = 15672
  }

  env = [
    "RABBITMQ_DEFAULT_USER=evreka",
    "RABBITMQ_DEFAULT_PASS=evreka"
  ]

  mounts {
    target = "/var/lib/rabbitmq"
    source = docker_volume.rabbitmq_data.name
    type   = "volume"
  }

  networks_advanced {
    name = var.network_name
    aliases = ["rabbitmq"]
  }
}