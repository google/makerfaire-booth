import numpy as np
from PIL import Image
import StringIO
import sqlite3
import tensorflow as tf
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define
import os

conn = sqlite3.connect('server.db')
c = conn.cursor()

sess = tf.InteractiveSession("grpc://localhost:2222")
model_dir = None
model_index = 1
saved_model_dir = "/tmp/retrain_arch_mobilenet_1.0_128/saved_models"
while os.path.exists(os.path.join(saved_model_dir, str(model_index))):
    model_index += 1
model_dir = os.path.join(saved_model_dir, str(model_index-1))
model = tf.saved_model.loader.load(
    sess,
    [tf.saved_model.tag_constants.SERVING],
    model_dir)
input_operation = sess.graph.get_operation_by_name('input')
output_operation = sess.graph.get_operation_by_name('final_result')

def img_to_array(img):
  return d

try:
    c.execute('''CREATE TABLE votes (burger CHARACTER(6), vote BOOLEAN)''')
except sqlite3.OperationalError, e:
    print "failed to create table", e
    pass

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('ok')

class VoteHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
                                            
    def get(self):
        burger = self.get_argument('burger', '000000')
        vote = bool(self.get_argument('vote', 'True'))
        c.execute("INSERT INTO votes VALUES (?, ?)", (burger, vote))
        conn.commit()

class PredictHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def post(self):
        file_body = self.request.files['filefieldname'][0]['body']
        img = Image.open(StringIO.StringIO(file_body))
        d = np.array(img).astype(np.float32)
        d = (d - 127.5)/127.5
        d = np.expand_dims(d[:, :, :3], 0)

        # TODO(dek): move the session-running logic to a thread which
        # does batched flushes with a timeout
        results = sess.run(output_operation.outputs[0], {
            input_operation.outputs[0]: d,
        })
        self.write(str(results))

urls = [
    (r"/", IndexHandler),
    (r"/vote", VoteHandler),
    (r"/predict", PredictHandler),
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
