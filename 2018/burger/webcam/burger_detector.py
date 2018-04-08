import tensorflow as tf

class BurgerDetector:
    def __init__(self):
        self.sess = tf.InteractiveSession()
        model = tf.saved_model.loader.load(
            self.sess,
            [tf.saved_model.tag_constants.SERVING],
            "/tmp/retrain_arch_mobilenet_1.0_128/saved_models/23")
        self.input_operation = self.sess.graph.get_operation_by_name('input')
        self.output_operation = self.sess.graph.get_operation_by_name('final_result')

    def detect(self, image):
        results = self.sess.run(self.output_operation.outputs[0], {
            self.input_operation.outputs[0]: image
        })
        print "%5.2f %5.2f" % (results[0][0], results[0][1])
