#!/usr/bin/env bash
set -e

IMAGE_NAME="formacao-svg"

docker build -t ${IMAGE_NAME} .

docker run --rm \
  -v "$(pwd):/app" \
  ${IMAGE_NAME}

ls -lh formacao.svg
