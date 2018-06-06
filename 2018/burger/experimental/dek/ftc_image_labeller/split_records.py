import tensorflow as tf
import random
flags = tf.app.flags
flags.DEFINE_string('train_output_path', 'records/train.records', 'Path to output training TFRecord')
flags.DEFINE_string('eval_output_path', 'records/eval.records', 'Path to output eval TFRecord')
flags.DEFINE_string('input_path', 'records/label.records', 'Path to input TFRecord')
flags.DEFINE_float('train_fraction', 0.7, 'Fraction of records to include in training set')
FLAGS = flags.FLAGS

def main(_):
  train_writer = tf.python_io.TFRecordWriter(FLAGS.train_output_path)
  eval_writer = tf.python_io.TFRecordWriter(FLAGS.eval_output_path)
  reader = tf.python_io.tf_record_iterator(FLAGS.input_path)
  for example in reader:
      writer = train_writer if random.random() < FLAGS.train_fraction else eval_writer
      writer.write(example)
  train_writer.close()
  eval_writer.close()

if __name__ == '__main__':
  tf.app.run()
