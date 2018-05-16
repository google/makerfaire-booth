import os
import pandas
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import sqlite3                           
import vote
import burger
import predict
import rank

train_burgers = pandas.read_hdf('../data/split.h5', 'train')
test_burgers = pandas.read_hdf('../data/split.h5', 'test')
connection = sqlite3.connect('../data/server.db')

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect("/static/index.html")


urls = [
    (r"/", IndexHandler),
    (r"/vote", vote.VoteHandler, dict(connection=connection)),
    (r"/burger", burger.BurgerHandler, dict(burgers=train_burgers)),
    (r"/predict", predict.PredictHandler),
    (r"/rank", rank.RankHandler, dict(burgers=train_burgers.append(test_burgers)))
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
