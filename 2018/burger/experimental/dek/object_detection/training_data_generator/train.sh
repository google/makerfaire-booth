# run from ~/workspace/models/research
# export PYTHONPATH=`pwd`:`pwd`/slim
python object_detection/train.py 	
  --logtostderr	\
  --pipeline_config_path=/home/dek/makerfaire-booth/2018/burger/experimental/dek/object_detection/training_data_generator/models/model/ssd_mobilenet_v1_burgers.config	 \
  --train_dir /home/dek/makerfaire-booth/2018/burger/experimental/dek/object_detection/training_data_generator/models/train
