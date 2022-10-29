#!/bin/bash

set -e
cd -- "$( dirname -- "${BASH_SOURCE[0]}" )"
export DOCKER_SCAN_SUGGEST=false

docker compose build --progress quiet resources && docker compose run --rm resources python /resource-manager.py $*
