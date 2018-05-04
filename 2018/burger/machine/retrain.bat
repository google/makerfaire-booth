set ARCH=mobilenet_1.0_128
set OUTDIR=c:\Users\dek\output\retrain_arch_%ARCH%
mkdir %OUTDIR%

python retrain.py   --image_height 128   --image_width 128   --image_dir c:/Users/dek/data/all   --output_graph %OUTDIR%/output_graph.pb   --bottleneck_dir %OUTDIR%/bottleneck   --intermediate_output_graphs_dir %OUTDIR%/intermediate   --summaries %OUTDIR%/summaries   --saved_model_dir %OUTDIR%/saved_models   --output_labels %OUTDIR%/output_labels.txt   --model_dir %OUTDIR%/model   --print_misclassified_test_images   --test_batch_size -1    --validation_batch_size -1   --validation_percentage 50   --how_many_training_steps 2500   --train_batch_size 256   --eval_step_interval 100   --architecture %ARCH%     --checkpoint_dir %OUTDIR%/checkpoints
  
