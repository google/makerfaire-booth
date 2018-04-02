# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os
import tensorflow as tf
import tensorflow as tf

    
def read_tensor_from_image_file(file_names,
                                input_height=299,
                                input_width=299,
                                input_mean=0,
                                input_std=255):
  input_name = "file_reader"
  output_name = "normalized"
  image_path = tf.placeholder(tf.string, None, 'image_path')
  file_reader = tf.read_file(image_path, input_name)
  # image_reader = tf.image.decode_png(
  #   file_reader, channels=3, name="png_reader")
  # float_caster = tf.cast(image_reader, tf.float32)
  # dims_expander = tf.expand_dims(float_caster, 0)
  # resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
  # normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
  sess = tf.Session()
  # result = sess.run(normalized)
  result = sess.run(file_reader, {image_path: [file_names]})

  return result



if __name__ == "__main__":
  prefix = "/home/dek/makerfaire-booth/2018/burger/machine/data/all/notburgers"
  file_name = os.path.join(prefix, "notburger0.png")
  file_name2 = os.path.join(prefix, "notburger1.png")
  model_file = \
    "tensorflow/examples/label_image/data/inception_v3_2016_08_28_frozen.pb"
  label_file = "tensorflow/examples/label_image/data/imagenet_slim_labels.txt"
  input_height = 299
  input_width = 299
  input_mean = 0
  input_std = 255

  file_names = [ file_name, file_name2 ]
  m = tf.map_fn(lambda f: tf.read_file(f),
                file_names)
  sess = tf.Session()
  result = sess.run(m)

  # t = read_tensor_from_image_file(
  #   [file_name, file_name2],
  #   input_height=input_height,
  #   input_width=input_width,
  #   input_mean=input_mean,
  #   input_std=input_std)
