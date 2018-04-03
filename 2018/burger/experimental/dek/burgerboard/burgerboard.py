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

def main(_):
  sess = tf.Session()
  with tf.device('/cpu:0'):
    t = read_tensor_from_image_file("/home/dek/makerfaire-booth/2018/burger/machine/data/all.299/burgers/burger_000156.png")

    image_shaped_input = tf.reshape(t, [-1, 299, 299, 3])

    X = tf.placeholder(tf.float32, [None, 299, 299, 3], name = "input")
    input_summary_op = tf.summary.image('input', image_shaped_input, 10)
    summary_results = sess.run(input_summary_op, feed_dict={X: t})
    writer = tf.summary.FileWriter('summaries')
    writer.add_graph(sess.graph)
    writer.add_summary(summary_results)
  
if __name__ == '__main__':
  unparsed = []
  tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)
