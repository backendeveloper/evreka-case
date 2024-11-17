resource "docker_network" "main_network" {
  name = "main_network"
}

module "traefik" {
  source       = "./modules/treafik"
  network_name = docker_network.main_network.name
}

module "postgres" {
  source       = "./modules/postgres"
  network_name = docker_network.main_network.name
}

module "rabbitmq" {
  source = "./modules/rabbitmq"
  network_name = docker_network.main_network.name
}

resource "docker_container" "gateway_api_container" {
  name  = "gateway-api"
  image = "gateway-api:latest"

  ports {
    internal = 8000
    external = 8083
  }

  env = [
    "RABBITMQ_QUEUE=task_queue",
    "RABBITMQ_HOST=rabbitmq",
    "RABBITMQ_PORT=5672",
    "RABBITMQ_USER=evreka",
    "RABBITMQ_PASSWORD=evreka",
  ]

  networks_advanced {
    name = docker_network.main_network.name
  }
}

resource "docker_container" "worker_api_container" {
  name  = "worker-api"
  image = "worker-api:latest"

  ports {
    internal = 8000
    external = 8084
  }

  env = [
    "RABBITMQ_QUEUE=task_queue",
    "RABBITMQ_HOST=rabbitmq",
    "RABBITMQ_PORT=5672",
    "RABBITMQ_USER=evreka",
    "RABBITMQ_PASSWORD=evreka",
    "POSTGRES_HOST=postgres",
    "POSTGRES_PORT=5432",
    "POSTGRES_USER=postgres",
    "POSTGRES_PASSWORD=postgres",
    "POSTGRES_DB=evreka-db"
  ]

  networks_advanced {
    name = docker_network.main_network.name
  }
}

resource "docker_container" "analytics_api_container" {
  name  = "analytics-api"
  image = "analytics-api:latest"

  ports {
    internal = 8000
    external = 8085
  }

  env = [
    "POSTGRES_HOST=postgres",
    "POSTGRES_PORT=5432",
    "POSTGRES_USER=postgres",
    "POSTGRES_PASSWORD=postgres",
    "POSTGRES_DB=evreka-db"
  ]

  networks_advanced {
    name = docker_network.main_network.name
  }
}