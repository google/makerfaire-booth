import sqlite3
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define
import os

conn = sqlite3.connect('server.db')
c = conn.cursor()


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

urls = [
    (r"/", IndexHandler),
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
