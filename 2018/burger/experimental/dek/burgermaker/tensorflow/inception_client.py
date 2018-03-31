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

from grpc.beta import implementations
import tensorflow as tf
import glob
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2
from PIL import Image
import numpy as np
import os

tf.app.flags.DEFINE_string('server', 'localhost:9000',
                           'PredictionService host:port')
tf.app.flags.DEFINE_string('image_dir', '', 'path containing images in PNG format')
FLAGS = tf.app.flags.FLAGS


def main(_):
  host, port = FLAGS.server.split(':')
  channel = implementations.insecure_channel(host, int(port))
  stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)
  # Send request
  pattern = os.path.join(FLAGS.image_dir, "*png")
  g = glob.glob(pattern)
  chunk = 100
  for i in range(0, len(g), chunk):
    x = []
    for j in range(i, i+chunk):
      img = Image.open(g[j]).convert('RGB')
      d = np.array(img).astype(np.float32)
      x.append(d)
    data = np.array(x)
    request = predict_pb2.PredictRequest()
    request.model_spec.name = 'inception'
    request.model_spec.signature_name = 'serving_default'
    proto = tf.contrib.util.make_tensor_proto(data, shape=data.shape)
    request.inputs['image'].CopyFrom(proto)
    result = stub.Predict(request, 120.0)  # 120 secs timeout
    print(result)


if __name__ == '__main__':
  tf.app.run()
