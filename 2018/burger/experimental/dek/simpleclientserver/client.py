import os
os.environ['CUDA_VISIBLE_DEVICES'] = ''
import numpy as np
import sys
import tensorflow as tf
from tensorflow.python.platform import gfile

def read_tensor_from_image_file(file_name,
                                input_height=299,
                                input_width=299,
                                input_mean=0,
                                input_std=255):
  input_name = "file_reader"
  output_name = "normalized"
  file_reader = tf.read_file(file_name, input_name)
  if file_name.endswith(".png"):
    image_reader = tf.image.decode_png(
        file_reader, channels=3, name="png_reader")
  elif file_name.endswith(".gif"):
    image_reader = tf.squeeze(
        tf.image.decode_gif(file_reader, name="gif_reader"))
  elif file_name.endswith(".bmp"):
    image_reader = tf.image.decode_bmp(file_reader, name="bmp_reader")
  else:
    image_reader = tf.image.decode_jpeg(
        file_reader, channels=3, name="jpeg_reader")
  float_caster = tf.cast(image_reader, tf.float32)
  dims_expander = tf.expand_dims(float_caster, 0)
  resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
  normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
  sess = tf.Session()
  result = sess.run(normalized)

  return result
def load_labels(label_file):
  label = []
  proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
  for l in proto_as_ascii_lines:
    label.append(l.rstrip())
  return label

def main(_):
  # a = tf.constant(5,name="a")
  # b = tf.constant(15,name="b")
  # c = tf.add(a,b,name="c")
  # p = tf.Print(c,[c])
    
  # sess.run(p)
  with tf.device('/cpu:0'):
    t = read_tensor_from_image_file("/home/dek/makerfaire-booth/2018/burger/machine/data/all.299/burgers/burger_000156.png")

  graph = tf.Graph()
  graph_def = tf.GraphDef()
  with tf.Graph().as_default() as graph:
    model_path = '/home/dek/tensorflow/tensorflow/examples/label_image/data/inception_v3_2016_08_28_frozen.pb'
    
    print('Model path: ', model_path)
    with open(model_path, "rb") as f:
      graph_def.ParseFromString(f.read())
    with graph.as_default():
      tf.import_graph_def(graph_def)
    input_op = graph.get_operation_by_name('import/input')
    output_op = graph.get_operation_by_name('import/InceptionV3/Predictions/Reshape_1')
    sess = tf.Session("grpc://localhost:2222")
    results = sess.run(output_op.outputs[0], {
      input_op.outputs[0]: t
    })
    results = np.squeeze(results)

    top_k = results.argsort()[-5:][::-1]
    label_file = "/home/dek/tensorflow/tensorflow/examples/label_image/data/imagenet_slim_labels.txt"
    labels = load_labels(label_file)
    for i in top_k:
      print(labels[i], results[i])
  
if __name__ == '__main__':
  unparsed = []
  tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)
