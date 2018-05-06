import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import vote
import burger

import sqlite3
connection = sqlite3.connect('server.db')


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('ok')

urls = [
    (r"/", IndexHandler),
    (r"/vote", vote.VoteHandler, dict(connection=connection)),
    (r"/burger", burger.BurgerHandler, dict(connection=connection)),
]

settings = dict({
        "debug": False,
    })

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(urls, **settings)
    http_server = tornado.httpserver.HTTPServer(app)

    http_server.listen(8888)
    tornado.ioloop.IOLoop.current().start()
