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
uvicorn canvass_api_model_store.main:app --host=0.0.0.0 --port=8000 "$RELOAD"
