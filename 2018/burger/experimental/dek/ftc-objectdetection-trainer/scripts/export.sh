MODELS_RESEARCH_DIR=/opt/tensorflow_models/research
export PYTHONPATH=$MODELS_RESEARCH_DIR:$MODELS_RESEARCH_DIR/slim

python $MODELS_RESEARCH_DIR/object_detection/export_inference_graph.py \
       --input_type=image_tensor \
       --pipeline_config_path=gs://ftc-research-object-detector-train/models/model/faster_rcnn_resnet101.config \
       --trained_checkpoint_prefix=gs://ftc-research-object-detector-train/models/train/model.ckpt-13450 \
       --output_directory=output_inference_graph
