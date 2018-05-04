source conf.sh
echo $PYTHONPATH
python convert.py \
  --train_output_path data/burgers_train.record \
  --eval_output_path data/burgers_eval.record \
