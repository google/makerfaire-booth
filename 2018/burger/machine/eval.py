from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
from datetime import datetime
import glob
import hashlib
import os.path
from PIL import Image
import pandas
import random
import re
import sys
import tarfile

import numpy as np
from six.moves import urllib
import tensorflow as tf

from tensorflow.python.framework import graph_util
from tensorflow.python.framework import tensor_shape
from tensorflow.python.platform import gfile

def img_to_array(filename):
  img = Image.open(filename).convert('RGB')
  d = np.array(img).astype(np.float32)
  d = (d - 127.5)/127.5
  return d

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--saved_model_dir',
      type=str,
      default='',
      help='Path to saved models.'
  )
  parser.add_argument(
      '--output',
      type=str,
      default='test.csv',
      help='Path to evaluated data output.'
  )
  parser.add_argument(
      '--data_dir',
      type=str,
      default='/home/dek/makerfaire-booth/2018/burger/machine/data/all',
      help='Path containing labelled data directories.'
  )

  FLAGS, unparsed = parser.parse_known_args()

  config=tf.ConfigProto()
  # allow_soft_placement=True,
  # log_device_placement=True)
  sess = tf.InteractiveSession(config=config)
  model_dir = None
  model_index = 1
  while os.path.exists(os.path.join(FLAGS.saved_model_dir, str(model_index))):
    model_index += 1
  print("Using model index:", model_index-1)
  model_dir = os.path.join(FLAGS.saved_model_dir, str(model_index-1))
  print("Using model dir:", model_dir)
  model = tf.saved_model.loader.load(
    sess,
    [tf.saved_model.tag_constants.SERVING],
    model_dir)
  
  burgers = []
  labels = []
  burger_p = []
  notburger_p = []
  predictions = []
  correct = []
  dir_ = []
  input_operation = sess.graph.get_operation_by_name('input')
  output_operation = sess.graph.get_operation_by_name('final_result')

  subdirs = os.listdir(FLAGS.data_dir)
  for type_ in subdirs:
    print "Label:", type_
    images=os.path.join(FLAGS.data_dir, type_)
    pattern = os.path.join(images, "*.png")
    g = glob.glob(pattern)

    chunk = 1000
    tensors = []
    for i in range(len(g)):
        item = g[i]
        t = img_to_array(item)
        tensors.append(t)

    for i in range(0, len(g), chunk):
        first = i
        last = i+chunk
        print(first,":",last)
        if last > len(g):
          last = len(g)
        results = sess.run(output_operation.outputs[0], {
            input_operation.outputs[0]: tensors[first:last]
        })
        for j, result in enumerate(results):
          burger = os.path.basename(g[i+j]).split(".")[0].split("_")[1]
          burger_p.append(result[0])
          notburger_p.append(result[1])
          burgers.append(burger)
          labels.append(type_)
          prediction = 'burgers' if result[0] > 0.5 else 'notburgers'
          predictions.append(prediction)
          correct.append(True if type_ == prediction else False)
          dir_.append('positive' if prediction is 'burgers' else 'negative')

  df = pandas.DataFrame(data = {
    'labels': labels,
    'prediction': predictions,
    'burger_p': burger_p,
    'notburger_p': notburger_p,
    'dir':dir_,
    'correct':correct,
  },
                        columns = ['labels', 'prediction', 'correct', 'dir', 'burger_p', 'notburger_p'],
                        index = burgers)
  df = df.sort_index()
  df.to_csv(FLAGS.output)
