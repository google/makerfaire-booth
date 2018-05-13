set MODELS_RESEARCH_DIR=z:\workspace\models\research
set PYTHONPATH=%MODELS_RESEARCH_DIR%;%MODELS_RESEARCH_DIR%\slim

python %MODELS_RESEARCH_DIR%/object_detection/eval.py  --logtostderr  --pipeline_config_path=models/model/faster_rcnn_resnet101_burgers.config  --checkpoint_dir=models/train  --eval_dir=models/eval
