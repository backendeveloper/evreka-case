resource "docker_volume" "traefik_data" {
  name = "traefik_data"
}

resource "docker_image" "traefik_image" {
  name = "traefik:v3.2"
}

resource "docker_container" "traefik" {
  name  = "traefik-gateway"
  image = docker_image.traefik_image.image_id

  command = [
    "--configFile=/traefik.yaml"
  ]

  # command = [
  #   "--api.insecure=true",
  #   "--providers.docker",
  #   # "--entrypoints.web.address=:80",
  #   # "--entrypoints.websecure.address=:443",
  #   # "--api.dashboard=true",
  #   # "--certificatesresolvers.myresolver.acme.httpchallenge=true",
  #   # "--certificatesresolvers.myresolver.acme.httpchallenge.entrypoint=web",
  #   # "--certificatesresolvers.myresolver.acme.email=youremail@example.com",
  #   # "--certificatesresolvers.myresolver.acme.storage=/letsencrypt/acme.json",
  #   # "--log.level=INFO",
  #   # "--accesslog=true",
  # ]

  labels {
    label   = "traefik.http.routers.traefik.rule"
    value = "Host('traefik.localhost')"
  }

  labels {
    label   = "traefik.http.routers.traefik.service"
    value = "api@internal"
  }

  labels {
    label   = "traefik.http.routers.traefik.entrypoints"
    value = "websecure"
  }

  labels {
    label   = "traefik.http.routers.traefik.tls.certresolver"
    value = "myresolver"
  }

  labels {
    label   = "traefik.http.routers.traefik.middlewares"
    value = "auth"
  }

  labels {
    label   = "traefik.http.middlewares.auth.basicauth.users"
    value = "admin:$$apr1$$H6uskkkW$$IgXLP6ewTrSuBkTrqE8wj/" # "admin:password"
  }

  ports {
    internal = 80
    external = 80
  }

  ports {
    internal = 8080
    external = 8080
  }

  mounts {
    target = "/traefik.yaml"
    source = abspath("${path.module}/config.yaml")
    type   = "bind"
  }

  volumes {
    host_path      = "/var/run/docker.sock"
    container_path = "/var/run/docker.sock"
    read_only      = true
  }

  volumes {
    volume_name    = docker_volume.traefik_data.name
    container_path = "/letsencrypt"
  }

  networks_advanced {
    name = var.network_name
    aliases = ["traefik"]
  }
}