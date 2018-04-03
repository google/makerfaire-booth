import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define
import os

import tensorflow as tf
# config = tf.ConfigProto(device_count={"CPU": 20}, inter_op_parallelism_threads=10, intra_op_parallelism_threads=10)
sess = tf.Session()#config=config)

class IndexHandler(tornado.web.RequestHandler):
    def initialize(self, thesess):
        self.sess = thesess

    def get(self):
        num = self.get_argument('num', 2)
        for i in range (100):
            ret = self.sess.run([asquare], feed_dict={a: num})
        self.write( 'result:' + str(ret))

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", IndexHandler,dict(thesess=sess))])
    http_server = tornado.httpserver.HTTPServer(app)

    http_server.bind(8888)
    http_server.start(10)
    tornado.ioloop.IOLoop.current().start()
