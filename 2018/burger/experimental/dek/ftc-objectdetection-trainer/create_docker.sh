#!/bin/bash
set -e

GCR_PREFIX=gcr.io/ftc-research/

# TODO(dek): add :1.0 to version tags?

cd containers

docker build . --build-arg TF_TAG=':latest' -t ${GCR_PREFIX}object-detection -f Dockerfile.base
docker build . --build-arg TF_TAG='@sha256:bfadad8f2c80424d8d6059d3b8cd6947bf23111dc786fc33db72b56b632a1f28' -t ${GCR_PREFIX}object-detection-gpu -f Dockerfile.base

docker push ${GCR_PREFIX}object-detection
docker push ${GCR_PREFIX}object-detection-gpu
# docker push ${GCR_PREFIX}/eval-gpu
