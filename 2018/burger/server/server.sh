python tf_server.py --saved_model_dir /tmp/retrain_arch_mobilenet_1.0_128/saved_models &
python server.py
curl -F 'filefieldname=@/home/dek/makerfaire-booth/2018/burger/machine/data/all/burgers/burger_123456.png' http://localhost:8888/predict
