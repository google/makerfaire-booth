import tensorflow as tf
import random
flags = tf.app.flags
flags.DEFINE_string('train_output_path', 'train.records', 'Path to output training TFRecord')
flags.DEFINE_string('eval_output_path', 'eval.records', 'Path to output eval TFRecord')
flags.DEFINE_string('input_path', 'label.records', 'Path to input TFRecord')
FLAGS = flags.FLAGS

def main(_):
  train_writer = tf.python_io.TFRecordWriter(FLAGS.train_output_path)
  eval_writer = tf.python_io.TFRecordWriter(FLAGS.eval_output_path)
  reader = tf.python_io.tf_record_iterator(FLAGS.input_path)
  for example in reader:
      writer = train_writer if random.random() < .7 else eval_writer
      writer.write(example)
  train_writer.close()
  eval_writer.close()

if __name__ == '__main__':
  tf.app.run()
