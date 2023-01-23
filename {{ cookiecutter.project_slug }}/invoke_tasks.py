"""Module to create kubernetes deployment config."""
from canvass_deployer import tasks
from invoke import Collection

CONFIG = {
    "azure_container_repo_name": "{{ cookiecutter.project_slug }}",
    "kubernetes_deployment_name": [
        # Needs to be updated to be the name of the k8s deployment
        # Cannot be the same as the project slug
        # For example: canvass-api-auth's k8s deployment is api-auth
        "{{ cookiecutter.project_slug }}",
    ],  # Has to be a list of strings.
}

ns = Collection.from_module(tasks, config={"project_config": CONFIG})
