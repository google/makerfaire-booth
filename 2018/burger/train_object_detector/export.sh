source conf.sh

python $MODELS_RESEARCH_DIR/object_detection/export_inference_graph.py \
       --input_type=image_tensor \
       --pipeline_config_path=models/model/faster_rcnn_resnet101_burgers.config \
       --trained_checkpoint_prefix=models/train/model.ckpt-1607 \
       --output_directory=output_inference_graph
       # --pipeline_config_path=models/model/ssd_mobilenet_v1_burgers.config \
