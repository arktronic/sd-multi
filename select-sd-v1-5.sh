#!/bin/bash

set -e
cd -- "$( dirname -- "${BASH_SOURCE[0]}" )"

[ -f "res/v1-5-pruned-emaonly.ckpt" ] || {
  echo Error: you do not have v1-5-pruned-emaonly.ckpt downloaded.
  echo Please download it using verify-resources.sh or manually before selecting.
  exit 1
}

ln -sf ./v1-5-pruned-emaonly.ckpt res/target-model.ckpt

