from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import tensorflow as tf

def main(_):
  tf.logging.set_verbosity(tf.logging.INFO)
  cluster = tf.train.ClusterSpec({"local": ["localhost:2222"]})
  server = tf.train.Server(cluster, job_name="local")
  server.join()
if __name__ == '__main__':
  unparsed = []
  tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)
