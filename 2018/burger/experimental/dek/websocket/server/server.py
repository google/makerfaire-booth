import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define
import tornado.websocket
import os


class EchoWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")

    def check_origin(self, origin):
        return True
    
    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        print("WebSocket closed")

urls = [
    (r"/websocket", EchoWebSocket),
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
