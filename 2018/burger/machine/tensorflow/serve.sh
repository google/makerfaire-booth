ARCH=mobilenet_1.0_128
OUTDIR=/tmp/retrain_arch_$ARCH
~/tensorflow/serving/bazel-bin/tensorflow_serving/model_servers/tensorflow_model_server --port=9000 --model_name=inception --model_base_path=$OUTDIR/saved_models --enable_batching
