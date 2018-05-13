import os
import pickle
import pandas
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import sqlite3                           
import vote
import burger
import validate

clf = pickle.load(open("clf.pkl", "rb"))
train_burgers = pandas.read_hdf('split.h5', 'train')
test_burgers = pandas.read_hdf('split.h5', 'test')
connection = sqlite3.connect('server.db')

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect("/static/index.html")


urls = [
    (r"/", IndexHandler),
    (r"/vote", vote.VoteHandler, dict(clf=clf, burgers=train_burgers, connection=connection)),
    (r"/validate", validate.ValidateHandler, dict(clf=clf, burgers=test_burgers)),
    (r"/burger", burger.BurgerHandler),
    (r"/static/(.*)",tornado.web.StaticFileHandler, {"path": "../static"}),
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
