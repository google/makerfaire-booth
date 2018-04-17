source conf.sh
python $MODELS_RESEARCH_DIR/object_detection/eval.py \
       --logtostderr \
       --pipeline_config_path=models/model/faster_rcnn_resnet101_burgers.config \
       --checkpoint_dir=models/train \
       --eval_dir=models/eval
       #--pipeline_config_path=models/model/ssd_mobilenet_v1_burgers.config \
