# ARCH=resnet_v1_50
ARCH=inception_v3
TRAIN_DIR=/tmp/burger-models/$ARCH
DATASET_DIR=/home/dek/makerfaire-booth/2018/burger/experimental/dek/burgermaker/data/all
PRETRAINED_CHECKPOINT_DIR=/tmp/checkpoints
# python convert_burgers.py
#   # --checkpoint_exclude_scopes=${ARCH}/logits \
#   # --trainable_scopes=${ARCH}/logits \
python train_image_classifier.py \
  --train_dir=${TRAIN_DIR} \
  --dataset_name=burgers \
  --dataset_split_name=train \
  --dataset_dir=${DATASET_DIR} \
  --model_name=${ARCH} \
  --checkpoint_path=${PRETRAINED_CHECKPOINT_DIR}/$ARCH.ckpt \
  --checkpoint_exclude_scopes=InceptionV3/Logits,InceptionV3/AuxLogits \
  --trainable_scopes=InceptionV3/Logits,InceptionV3/AuxLogits \
  --max_number_of_steps=1000 \
  --batch_size=32 \
  --learning_rate=0.01 \
  --save_interval_secs=60 \
  --save_summaries_secs=60 \
  --log_every_n_steps=100 \
  --optimizer=rmsprop \
  --weight_decay=0.00004

# python eval_image_classifier.py \
#   --checkpoint_path=${TRAIN_DIR} \
#   --eval_dir=${TRAIN_DIR} \
#   --dataset_name=burgers \
#   --dataset_split_name=validation \
#   --dataset_dir=${DATASET_DIR} \
#   --model_name=$ARCH
