source conf.sh
python $MODELS_RESEARCH_DIR/object_detection/eval.py \
       --logtostderr \
       --pipeline_config_path=models/model/faster_rcnn_resnet101_burgers.config \
       --checkpoint_dir=gs://seventh-oven-198801-burgers/models/train \
       --eval_dir=gs://seventh-oven-198801-burgers/models/eval
