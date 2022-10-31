#!/bin/bash

set -e
cd -- "$( dirname -- "${BASH_SOURCE[0]}" )"
export DOCKER_SCAN_SUGGEST=false

echo -e "\n\nNOTE: The amotile-backend process will continually crash while AUTOMATIC1111 is starting.\nThis is expected. Just wait a bit.\n\n"
sleep 2

docker compose --profile amotile up --build
