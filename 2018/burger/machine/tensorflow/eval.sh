ARCH=mobilenet_1.0_128
OUTDIR=/tmp/retrain_arch_$ARCH
#!/bin/sh
python eval.py \
  --image_height 128 \
  --image_width 128 \
  --image_dir ~/makerfaire-booth/2018/burger/machine/data/all \
  --output_graph $OUTDIR/output_graph.pb \
  --bottleneck_dir $OUTDIR/bottleneck \
  --intermediate_output_graphs_dir $OUTDIR/intermediate \
  --summaries $OUTDIR/summaries \
  --saved_model_dir $OUTDIR/saved_models \
  --output_labels $OUTDIR/output_labels.txt \
  --model_dir $OUTDIR/model  \
  --print_misclassified_test_images \
  --test_batch_size -1   \
  --validation_batch_size -1 \
  --how_many_training_steps 10000 \
  --train_batch_size 512 \
  --eval_step_interval 500 \
  --architecture $ARCH
