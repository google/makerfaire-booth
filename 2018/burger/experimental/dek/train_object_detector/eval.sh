python object_detection/eval.py \
       --logtostderr \
       --pipeline_config_path=models/model/ssd_mobilenet_v1_burgers.config \
       --checkpoint_dir=models/train \
       --eval_dir=eval
