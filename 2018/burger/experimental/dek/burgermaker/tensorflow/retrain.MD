python tensorflow/examples/image_retraining/retrain.py --image_dir ~/makerfaire-booth/2018/burger/experimental/dek/burgermaker/data/all --output_graph /tmp/retrain/output_graph.pb --bottleneck_dir /tmp/retrain/bottleneck --intermediate_output_graphs_dir /tmp/retrain/intermediate --summaries /tmp/retrain/summaries --saved_model_dir /tmp/retrain/saved_models --output_labels /tmp/retrain/output_labels.txt --model_dir /tmp/retrain/model


python tensorflow/examples/label_image/label_image.py --graph=/tmp/retrain/output_graph.pb --labels=/tmp/retrain/output_labels.txt --input_layer=Mul --output_layer=final_result --input_mean=128 --input_std=128 --image=/home/dek/makerfaire-booth/2018/burger/experimental/dek/burgermaker/data/all/burgers/burger00003.png
