from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
from datetime import datetime
import glob
import hashlib
import os.path
from PIL import Image
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

config=tf.ConfigProto(allow_soft_placement=True,
                      log_device_placement=True)
sess = tf.InteractiveSession(config=config)
model = tf.saved_model.loader.load(
    sess,
    [tf.saved_model.tag_constants.SERVING],
    "/tmp/retrain_arch_mobilenet_1.0_128/saved_models/20")

# TODO(dek): figure out how to combine all the results into pandas df
for type_ in 'burgers', 'notburgers':
    images=os.path.join("/home/dek/makerfaire-booth/2018/burger/machine/data/all/%s" % type_)
    pattern = os.path.join(images, "*.png")
    g = glob.glob(pattern)


    input_operation = sess.graph.get_operation_by_name('input')
    output_operation = sess.graph.get_operation_by_name('final_result')
    chunk = 1000
    results = []
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
        result = sess.run(output_operation.outputs[0], {
            input_operation.outputs[0]: tensors[first:last]
        })
        results.extend(result)

