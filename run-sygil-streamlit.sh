#!/bin/bash

set -e
cd -- "$( dirname -- "${BASH_SOURCE[0]}" )"
export DOCKER_SCAN_SUGGEST=false

export SD_MULTI_SYGIL_COMMAND="bash -c 'python -m streamlit run scripts/webui_streamlit.py'"
docker compose --profile sygil up --build
