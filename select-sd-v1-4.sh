#!/bin/bash

set -e
cd -- "$( dirname -- "${BASH_SOURCE[0]}" )"

[ -f "res/sd-v1-4.ckpt" ] || {
  echo Error: you do not have sd-v1-4.ckpt downloaded.
  echo Please download it using verify-resources.sh or manually before selecting.
  exit 1
}

ln -sf ./sd-v1-4.ckpt res/target-model.ckpt

