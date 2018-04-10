import os

import numpy as np
from PIL import Image
import tensorflow as tf
import StringIO
import tornado.web

def img_to_array(img):
  return d

sess = tf.InteractiveSession("grpc://localhost:2222")
train_op = tf.no_op('train')
options = tf.RunOptions(timeout_in_ms=1000)
result = sess.run([train_op], None,
                  options=options)

model_dir = None
model_index = 1
saved_model_dir = "/tmp/retrain_arch_mobilenet_1.0_128/saved_models"
while os.path.exists(os.path.join(saved_model_dir, str(model_index))):
    model_index += 1
model_dir = os.path.join(saved_model_dir, str(model_index-1))
model = tf.saved_model.loader.load(
    sess,
    [tf.saved_model.tag_constants.SERVING],
    model_dir)
input_operation = sess.graph.get_operation_by_name('input')
output_operation = sess.graph.get_operation_by_name('final_result')
class PredictHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def post(self):
        file_body = self.request.files['filefieldname'][0]['body']
        img = Image.open(StringIO.StringIO(file_body))
        d = np.array(img).astype(np.float32)
        d = (d - 127.5)/127.5
        d = np.expand_dims(d[:, :, :3], 0)

        # TODO(dek): move the session-running logic to a thread which
        # does batched flushes with a timeout
        options = tf.RunOptions(timeout_in_ms=1000)
        results = sess.run(output_operation.outputs[0], { input_operation.outputs[0]: d, },
                           options=options)
        self.write(str(results))

