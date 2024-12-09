# Makefile

DOCKER_COMPOSE = docker compose
DAEMONIZE =


up:
	@$(DOCKER_COMPOSE) up

down:
	@$(DOCKER_COMPOSE) down

restart:
	@$(DOCKER_COMPOSE) down
	@$(DOCKER_COMPOSE) up --build $(DAEMONIZE)


restart-d:
	$(eval DAEMONIZE = -d)
	@$(MAKE) restart

