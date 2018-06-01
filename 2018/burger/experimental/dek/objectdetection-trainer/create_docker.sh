#!/bin/bash
set -e

GCR_PREFIX=gcr.io/seventh-oven-198801

# TODO(dek): add :1.0 to version tags?

docker build . --build-arg TF_TAG=':latest' -t object-detection-base -f Dockerfile.base
docker build . --build-arg TF_TAG='@sha256:bfadad8f2c80424d8d6059d3b8cd6947bf23111dc786fc33db72b56b632a1f28' -t object-detection-base-gpu -f Dockerfile.base

docker build . --build-arg GPU_TAG='' -t ${GCR_PREFIX}/trainer -f Dockerfile.trainer
docker build . --build-arg GPU_TAG='-gpu' -t ${GCR_PREFIX}/trainer-gpu -f Dockerfile.trainer

docker build . -t ${GCR_PREFIX}/eval-gpu -f Dockerfile.eval-gpu

docker push ${GCR_PREFIX}/trainer
docker push ${GCR_PREFIX}/trainer-gpu
docker push ${GCR_PREFIX}/eval-gpu
