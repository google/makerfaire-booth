set MODELS_RESEARCH_DIR=z:\workspace\models\research
set PYTHONPATH=%MODELS_RESEARCH_DIR%;%MODELS_RESEARCH_DIR%\slim
python convert.py  --train_output_path ../data/burgers_train.record  --eval_output_path ../data/burgers_eval.record
