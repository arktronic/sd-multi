#!/bin/bash

set -e
cd -- "$( dirname -- "${BASH_SOURCE[0]}" )"
export DOCKER_SCAN_SUGGEST=false

docker compose build invokeai
docker compose run --service-ports --rm invokeai bash -c 'python scripts/invoke.py'
