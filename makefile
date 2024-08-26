# Define as variáveis para facilitar a reutilização
COMPOSE_FILE=docker-compose.yml
PYTHON_FILE=app.py
API_ENDPOINT=http://localhost:5000/data
CONTENT_TYPE="Content-Type: application/json"

all: up install run

up:
	docker-compose -f $(COMPOSE_FILE) up -d

install:
	poetry install

run:
	poetry run python $(PYTHON_FILE)

curl:
	curl -X POST $(API_ENDPOINT) -H $(CONTENT_TYPE)

test:
	poetry run pytest

down:
	docker-compose -f $(COMPOSE_FILE) down