import os
import pandas
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import sqlite3                           
import reset
import vote
import rank
import burger
import sys
sys.path.insert(0, '../model')
from model2 import Model

model = Model()

train_burgers = pandas.read_hdf('../data/split.h5', 'train')
test_burgers = pandas.read_hdf('../data/split.h5', 'test')
connection = sqlite3.connect('../data/server.db')
burgers = train_burgers.append(test_burgers)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect("/static/index.html")


urls = [
    (r"/", IndexHandler),
    (r"/reset", reset.ResetHandler, dict(connection=connection, model=model)),
    (r"/vote", vote.VoteHandler, dict(connection=connection, burgers=burgers, model=model)),
    (r"/rank", rank.RankHandler, dict(connection=connection, burgers=burgers, model=model)),
    (r"/burger", burger.BurgerHandler, dict(burgers=train_burgers)),
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
