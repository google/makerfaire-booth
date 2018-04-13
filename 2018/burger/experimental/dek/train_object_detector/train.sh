source conf.sh
python $MODELS_RESEARCH_DIR/object_detection/train.py \
  --logtostderr	\
  --pipeline_config_path=models/model/ssd_mobilenet_v1_burgers.config	 \
  --train_dir=models/train
