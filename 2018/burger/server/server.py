import sqlite3
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define
import os
os.environ["CUDA_VISIBLE_DEVICES"]="-1"

import tensorflow as tf
# config = tf.ConfigProto(device_count={"CPU": 20}, inter_op_parallelism_threads=10, intra_op_parallelism_threads=10)
sess = tf.Session()#config=config)

conn = sqlite3.connect('server.db')
c = conn.cursor()


try:
    c.execute('''CREATE TABLE votes (burger CHARACTER(6), vote BOOLEAN)''')
except sqlite3.OperationalError, e:
    print "failed to create table", e
    pass

class IndexHandler(tornado.web.RequestHandler):
    def initialize(self, thesess):
        self.sess = thesess

    def get(self):
        num = self.get_argument('num', 2)
        for i in range (100):
            ret = self.sess.run([asquare], feed_dict={a: num})
        self.write( 'result:' + str(ret))

class VoteHandler(tornado.web.RequestHandler):
    def get(self):
        burger = self.get_argument('burger', '000000')
        vote = bool(self.get_argument('vote', 'True'))
        c.execute("INSERT INTO votes VALUES (?, ?)", (burger, vote))
        conn.commit()

urls = [
    (r"/", IndexHandler, dict(thesess=sess)),
    (r"/vote", VoteHandler),
]

settings = dict({
        "debug": False,
    })
if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(urls, **settings)
    http_server = tornado.httpserver.HTTPServer(app)

    http_server.bind(8888)
    http_server.start(10)
    tornado.ioloop.IOLoop.current().start()
