import tensorflow as tf

if __name__ == '__main__':
  cluster = tf.train.ClusterSpec({"local": ["localhost:2222"]})
  server = tf.train.Server(cluster, job_name="local")
  server.join()
