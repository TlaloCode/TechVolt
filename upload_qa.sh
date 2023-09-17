#!/bin/bash

# Descarga la última versión del proyecto
git pull origin develop

# Ejecuta un backup de la BDD
docker-compose -f docker-compose.qa.yml exec -T postgres backup
docker-compose -f docker-compose.qa.yml run -T --rm awscli upload

# Instala la nueva versión del proyecto
docker-compose -f docker-compose.qa.yml up --build -d -V --force-recreate

# Limpia Docker
docker system prune --volumes -f
