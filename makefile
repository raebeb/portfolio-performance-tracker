DC = docker-compose
.PHONY: help

# Show help
help:
	@echo "Comandos disponibles:"
	@echo "  make up               Levantar todos los contenedores con build"
	@echo "  make start            Levantar contenedores sin build"
	@echo "  make stop             Detener todos los contenedores"
	@echo "  make rebuild-front    Rebuild solo frontend"
	@echo "  make rebuild-back     Rebuild solo backend"
	@echo "  make migrate          Ejecutar migraciones en backend"
	@echo "  make makemigrations   Crear nuevas migraciones en backend"
	@echo "  make shell            Acceder a bash en el contenedor backend"
	@echo "  make py-shell         Abrir Django shell"
	@echo "  make logs             Ver logs en tiempo real"
	@echo "  make etl file=path    Ejecutar ETL con archivo Excel (ej: make etl file=data/datos.xlsx)"
	@echo "  make test             Ejecutar tests con pytest"
	@echo "  make nuke             Borrar contenedores, volúmenes y huérfanos"

# Make 'help' the default target
.DEFAULT_GOAL := help

# lift up all the containers and build them
up:
	$(DC) up --build

# just lift up all the containers
start:
	$(DC) up

# stop all the containers
stop:
	$(DC) down

# rebuild front
rebuild-front:
	$(DC) build frontend

# rebuild back
rebuild-back:
	$(DC) build backend

# run migrations
migrate:
	$(DC) exec backend python manage.py migrate

# make migrations
makemigrations:
	$(DC) exec backend python manage.py makemigrations

# backend shell
shell:
	$(DC) exec backend bash

# django shell
py-shell:
	$(DC) exec backend python manage.py shell

# show logs
logs:
	$(DC) logs -f

# run etl
etl:
	$(DC) exec backend python manage.py load_excel_data $(file)

test:
	$(DC) exec backend pytest

# destroy all containers and volumes
nuke:
	$(DC) down -v --remove-orphans
