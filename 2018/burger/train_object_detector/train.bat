set MODELS_RESEARCH_DIR=z:\workspace\models\research
set PYTHONPATH=%MODELS_RESEARCH_DIR%;%MODELS_RESEARCH_DIR%\slim
python %MODELS_RESEARCH_DIR%/object_detection/train.py --logtostderr train --pipeline_config_path=models/model/faster_rcnn_resnet101_burgers.config --train_dir=models/train
