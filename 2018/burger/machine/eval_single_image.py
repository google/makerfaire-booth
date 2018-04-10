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
      '--filename',
      type=str,
      default='',
      help='Filename of image.'
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
  
  input_operation = sess.graph.get_operation_by_name('input')
  output_operation = sess.graph.get_operation_by_name('final_result')

  t = img_to_array(FLAGS.filename)
  results = sess.run(output_operation.outputs[0], {
      input_operation.outputs[0]: [t],
  })
  print(results)
