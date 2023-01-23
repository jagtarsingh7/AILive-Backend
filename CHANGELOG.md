# CHANGELOG
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [LATEST]

## [0.3.4] - 2022-12-16
### Added
- Added health endpoints
- Hot reload added
### Fixed
- PR template name change to allow github to detect it
## [0.3.3] - 2022-12-16
### Added
### Changed
- updated skjold from v0.5.0 to v0.6.0
### Deprecated
### Removed
### Fixed

## [0.3.2] - 2022-12-01
### Added
- set env vars step for CI
### Changed
### Deprecated
### Removed
### Fixed
- fix resource class

## [0.3.1] - 2022-12-01
### Added
- Swapped Dev and project dependencies
### Changed
- Changed the circleCI resource class to small
### Deprecated
### Removed
- CircleCI performance build steps
### Fixed


## [0.3.0] - 2022-11-16
### Added
- ORM support with SQLAlchemy
- Database migrations with Alembic
- Canvass FastAPI as dependency library
- Docker BuildKit support for SSH-based private package repositories
- Makefile commands for upgrading dependencies, and migrating the database
- PostgreSQL service in docker-compose.yml
- FactoryBoy for generating test data
### Changed
- create_app() now uses method from Canvass FastAPI library
- Unified `conftest.py` for all tests
- Moved `tests` directory to `{{ cookiecutter.project_module }}/tests`
### Deprecated
### Removed
- Health endpoints
### Fixed
- Dependencies installation in `post_gen_project.py`
- Initial commit in `post_gen_project.py`

## [0.2.0] - 2022-11-16
### Added
- Pre-commit hook to check presence and format of docstrings
### Changed
### Deprecated
### Removed
### Fixed

## [0.1.1] - 2022-10-07
### Added
- Poetry commands with Docker Compose to `Makefile`
### Changed
- README.md with instructions on how to use Poetry commands from Makefile
- `docker-compose` command in `Makefile` to use `docker compose`
### Deprecated
### Removed
### Fixed

## [0.1.0] - 2022-09-29
### Added
- Initial release
### Changed
### Deprecated
### Removed
### Fixed
