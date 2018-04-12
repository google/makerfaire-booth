python object_detection/export_inference_graph.py \
       --input_type=image_tensor \
       --pipeline_config_path=/home/dek/makerfaire-booth/2018/burger/experimental/dek/object_detection/training_data_generator/models/model/ssd_mobilenet_v1_burgers.config \
       --trained_checkpoint_prefix=/home/dek/makerfaire-booth/2018/burger/experimental/dek/object_detection/training_data_generator/models/train/model.ckpt-0 \
       --output_directory=output_inference_graph.pb
