
init:
	cp template.env .env
	pre-commit install
	$(MAKE) build

lint:
	pre-commit install && pre-commit run -a -v

build:
	docker compose build

run:
	docker compose up

stop:
	docker compose down

add: DEPENDENCY ?= $(shell bash -c 'read -p "Dependency: " dependency; echo $$dependency')
add:
	docker compose run api poetry add $(DEPENDENCY)
	$(MAKE) build

add-dev: DEPENDENCY ?= $(shell bash -c 'read -p "Dependency: " dependency; echo $$dependency')
add-dev:
	docker compose run api poetry add --group dev $(DEPENDENCY)
	$(MAKE) build

remove: DEPENDENCY ?= $(shell bash -c 'read -p "Dependency: " dependency; echo $$dependency')
remove:
	docker compose run api poetry remove $(DEPENDENCY)
	$(MAKE) build

update:
	docker compose run api poetry update
	$(MAKE) build

migrations:
	@read -p "Enter the name of the new migration: " migration_name; \
	docker compose run api alembic revision --autogenerate -m "$$migration_name"

migrate:
	docker compose run api alembic upgrade head

lock:
	docker compose run api poetry lock

test:
	docker compose run api poetry run pytest -n auto -vv

test-cov:
	docker compose run api poetry run pytest -vv --cov=canvass_api_model_store --cov-report=term-missing

test-cov-html:
	docker compose run api poetry run pytest -vv --cov=canvass_api_model_store --cov-report=html

test-cov-ci:
	poetry run pytest -vv --cov=canvass_api_model_store --cov-report=html

clean:
	rm -rf .cache
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf htmlcov
	rm -rf .tox/
	rm -rf docs/_build
	@find . -name '*.pyc' -exec rm -rf {} \;
	@find . -name '__pycache__' -exec rm -rf {} \;
	@find . -name 'Thumbs.db' -exec rm -rf {} \;
	@find . -name '*~' -exec rm -rf {} \;
