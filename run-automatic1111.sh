#!/bin/bash

set -e
cd -- "$( dirname -- "${BASH_SOURCE[0]}" )"
export DOCKER_SCAN_SUGGEST=false

docker compose --profile auto up --build
