# Canvass API Cookiecutter

Canvass API Cookiecutter is a template for building production-ready FastAPI application quickly.

## Features
- Web framework FastAPI
- Custom Python version
- Uses Poetry for dependency management
- Renders FastAPI projects with 100% starting test coverage
- Optimized development and production settings
- Docker support using docker-compose for development and helm-charts for production
- Run tests with unittest or pytest
- CI (continuous integration) pipeline with CircleCI
- CORS (Cross Origin Resource Sharing).
- Default integration with:
  - pre-commit for identifying simple issues before submission to code review
  - black for code formatting
  - flake8 for identifying and reporting on style issues
  - isort for sorting imports
  - mypy for static type checking
  - pytest for testing
  - pytest-cov for test coverage
  - pytest-mock for mocking
  - pytest-asyncio for async testing
  - pytest-xdist for parallel testing
  - pydoctest for ensure docstrings are included in new code

### Optional integrations (future work)
- SQLAlchemy models
- Alembic migrations
- Celery worker that can import and use models and code from the rest of the backend selectively.
- Flower for Celery jobs monitoring.

## Requirements
- [docker](https://docs.docker.com/get-docker/)
- [docker-compose](https://docs.docker.com/compose/install/)
- [pre-commit](https://pre-commit.com/#install)
- [cookiecutter](https://cookiecutter.readthedocs.io/en/latest/installation.html)

## How to use it
### Install cookiecutter
```bash
pipx install cookiecutter
```
### Install pre-commit
```bash
pipx install pre-commit
```
### Create a new project
```bash
cookiecutter gh:canvassanalytics/canvass-api-cookiecutter
```
### Run the project
```bash
cd <project_name>
make run
```
### Run tests
```bash
make test
```
### Run tests with coverage
```bash
make test-cov
```
### Run tests with coverage and HTML report
```bash
make test-cov-html
```
