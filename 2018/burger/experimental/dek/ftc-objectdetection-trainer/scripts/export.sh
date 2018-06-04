#!/bin/sh
MODELS_RESEARCH_DIR=/opt/tensorflow_models/research
export PYTHONPATH=$MODELS_RESEARCH_DIR:$MODELS_RESEARCH_DIR/slim
export GS_PREFIX=gs://ftc-research-object-detector-train/
python $MODELS_RESEARCH_DIR/object_detection/export_inference_graph.py \
       --input_type=image_tensor \
       --pipeline_config_path=${GS_PREFIX}models/model/faster_rcnn_resnet101.config \
       --trained_checkpoint_prefix=${GS_PREFIX}models/train/model.ckpt-47889 \
       --output_directory=output_inference_graph
