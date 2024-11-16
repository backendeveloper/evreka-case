resource "docker_network" "main_network" {
  name = "main_network"
}

module "traefik" {
  source       = "./modules/treafik"
  network_name = docker_network.main_network.name
}

module "rabbitmq" {
  source = "./modules/rabbitmq"
  network_name = docker_network.main_network.name
}