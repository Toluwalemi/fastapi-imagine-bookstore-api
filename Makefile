COMPOSE = docker-compose

SERVICE = web

up-build:
	$(COMPOSE) up -d --build

build:
	$(COMPOSE) build

rebuild:
	$(COMPOSE) build --no-cache

up:
	$(COMPOSE) up

up-d:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

enter:
	$(COMPOSE) exec $(bookstore-web) bash

pre-commit:
	pre-commit run --all-files
