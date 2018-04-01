# Copyright 2016 Google Inc. All Rights Reserved.
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

#!/usr/bin/env python2.7

"""Send JPEG image to tensorflow_model_server loaded with inception model.
"""

from __future__ import print_function

# This is a placeholder for a Google-internal import.

import pandas
from grpc.beta import implementations
import tensorflow as tf
import glob
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2
from PIL import Image
import numpy as np
import os
from multiprocessing import Pool

tf.app.flags.DEFINE_string('server', 'localhost:9000',
                           'PredictionService host:port')
tf.app.flags.DEFINE_string('image_dir', '', 'path containing images in PNG format')
tf.app.flags.DEFINE_string('label', '', 'label of burger/notburger')
FLAGS = tf.app.flags.FLAGS

def img_to_array(filename):
  img = Image.open(filename).convert('RGB')
  d = np.array(img).astype(np.float32)
  d = (d - 127.5)/127.5
  return d

def main(_):
  host, port = FLAGS.server.split(':')
  channel = implementations.insecure_channel(host, int(port))
  stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)
  # Send request
  pattern = os.path.join(FLAGS.image_dir, "*png")
  g = glob.glob(pattern)
  keys = [os.path.basename(file_).split('_')[1].split(".")[0] for file_ in g]
  x = map(img_to_array, g)
  print("Read all files")
  x = np.array(x)
  print("Converted all files to numpy")
  chunk = 1000
  results = []
  preds = np.zeros( (len(x), 2), dtype=float)
  for i in range(0, len(x), chunk):
    print(i, "of", len(x))
    first = i
    last = i+chunk
    if last > len(x):
      last = len(x)
    data = x[first:last]
    request = predict_pb2.PredictRequest()
    request.model_spec.name = 'inception'
    request.model_spec.signature_name = 'serving_default'
    proto = tf.contrib.util.make_tensor_proto(data, shape=data.shape)
    request.inputs['image'].CopyFrom(proto)
    result = stub.Predict(request, 120.0)  # 120 secs timeout
    p = list(result.outputs['prediction'].float_val)
    p = np.array(p).reshape(last-first, 2)
    preds[first:last] = p

  labels = [FLAGS.label] * preds.shape[0]
  df = pandas.DataFrame(data = {
    'notburger_p': preds[:,0],
    'burger_p': preds[:,1],
    'label': labels,
    },
                        columns = ['label','notburger_p', 'burger_p'],
                        index=keys)
  df.to_csv("predictions.csv", index_label='key')

if __name__ == '__main__':
  tf.app.run()
