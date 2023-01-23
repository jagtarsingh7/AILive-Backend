import os
from pathlib import Path

PRODUCTION_DEPENDENCIES = [
    "fastapi",
    "uvicorn",
    "sqlmodel",
    "alembic",
    "asyncpg",
    "git+ssh://git@github.com:canvassanalytics/canvass-fastapi.git",
]

DEVELOPMENT_DEPENDENCIES = [
    "pytest",
    "pytest-asyncio",
    "pytest-cov",
    "pytest-mock",
    "pytest-sugar",
    '"pytest-xdist[psutil]"',
    "requests",
    "Faker",
    "aiosqlite",
    "factory-boy",
]


def init_git_repository():
    os.system("git init")
    os.system("git checkout -b dev")


def first_commit():
    os.system("git add --all")
    os.system("git commit -m 'First commit'")


def init_project():
    os.system("make init")
    print("Project initialized")


def lint():
    os.system("git add --all")
    os.system("make lint")


def run_project():
    print("Run the following to run the project: make run")


def fix_shell_scripts_endings():
    path: Path
    for path in Path(".").glob("**/*.sh"):
        data = path.read_bytes()
        lf_data = data.replace(b"\r\n", b"\n")
        path.write_bytes(lf_data)


def install_dependencies():
    print("Installing dependencies...")
    development_dependencies = " ".join(DEVELOPMENT_DEPENDENCIES)
    os.system(f"DEPENDENCY='{development_dependencies}' make add-dev")
    production_dependencies = " ".join(PRODUCTION_DEPENDENCIES)
    os.system(f"DEPENDENCY='{production_dependencies}' make add")
    print("Dependencies installed")


if __name__ == "__main__":
    fix_shell_scripts_endings()
    init_git_repository()
    init_project()
    install_dependencies()
    lint()
    first_commit()
    print("Project successfully created.")
