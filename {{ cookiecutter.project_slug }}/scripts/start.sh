#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

RELOAD=""
DEBUG_MODE=${DEBUG:-false}
if [ "$DEBUG_MODE" = true ]; then
    RELOAD="--reload"
    echo "Enabling Hot reload of API"
fi
uvicorn {{ cookiecutter.project_module }}.main:app --host={{cookiecutter.api_host}} --port={{cookiecutter.api_port}} "$RELOAD"
