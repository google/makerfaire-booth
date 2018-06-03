#!/bin/sh
MODELS_RESEARCH_DIR=/opt/tensorflow_models/research
export PYTHONPATH=$MODELS_RESEARCH_DIR:$MODELS_RESEARCH_DIR/slim
export GS_PREFIX=gs://ftc-research-object-detector-train/
python $MODELS_RESEARCH_DIR/object_detection/eval.py \
       --pipeline_config_path=${GS_PREFIX}models/model/faster_rcnn_resnet101.config \
       --checkpoint_dir=${GS_PREFIX}models/train \
       --eval_dir=${GS_PREFIX}models/eval
