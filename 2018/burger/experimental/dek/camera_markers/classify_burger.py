import numpy as np
from PIL import Image
import os
import tensorflow as tf

from tensorflow.python.framework import graph_util
from tensorflow.python.framework import tensor_shape
from tensorflow.python.platform import gfile

def filename_to_img(filename):
  img = Image.open(filename).convert('RGB')
  return img

def img_to_array(img):
  d = np.array(img).astype(np.float32)
  d = (d - 127.5)/127.5
  return d

SAVED_MODEL_DIR="../../../machine/saved_models"

class BurgerClassifier(object):
    def __init__(self):
        config=tf.ConfigProto()
        # allow_soft_placement=True,
        # log_device_placement=True)
        self.sess = tf.InteractiveSession(config=config)

        model_dir = None
        model_index = 1
        while os.path.exists(os.path.join(SAVED_MODEL_DIR, str(model_index))):
            model_index += 1
        print("Using model index:", model_index-1)
        model_dir = os.path.join(SAVED_MODEL_DIR, str(model_index-1))
        print("Using model dir:", model_dir)
        model = tf.saved_model.loader.load(
            self.sess,
            [tf.saved_model.tag_constants.SERVING],
            model_dir)

        self.input_operation = self.sess.graph.get_operation_by_name('input')
        self.output_operation = self.sess.graph.get_operation_by_name('final_result')

    def classify(self, image):
        results = self.sess.run(self.output_operation.outputs[0], {
            self.input_operation.outputs[0]: [image],
        })
        return results

if __name__ == '__main__':
    b = BurgerClassifier()
    filename = "image.png"
    img = filename_to_img(filename)
    array = img_to_array(img)
    results = b.classify(array)
    print(results)
