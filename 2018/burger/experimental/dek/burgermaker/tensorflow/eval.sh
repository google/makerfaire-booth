#!/bin/sh
python eval.py \
  --image_height 128 \
  --image_width 128 \
  --image_dir ~/makerfaire-booth/2018/burger/experimental/dek/burgermaker/data/all \
  --output_graph /tmp/retrain_arch_mobilenet_1.0_128_quant/output_graph.pb \
  --bottleneck_dir /tmp/retrain_arch_mobilenet_1.0_128_quant/bottleneck \
  --intermediate_output_graphs_dir /tmp/retrain_arch_mobilenet_1.0_128_quant/intermediate \
  --summaries /tmp/retrain_arch_mobilenet_1.0_128_quant/summaries \
  --saved_model_dir /tmp/retrain_arch_mobilenet_1.0_128_quant/saved_models \
  --output_labels /tmp/retrain_arch_mobilenet_1.0_128_quant/output_labels.txt \
  --model_dir /tmp/retrain_arch_mobilenet_1.0_128_quant/model  \
  --print_misclassified_test_images \
  --test_batch_size -1   \
  --validation_batch_size -1 \
  --how_many_training_steps 10000 \
  --train_batch_size 512 \
  --eval_step_interval 500 \
  --architecture mobilenet_1.0_128_quant
