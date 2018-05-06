from __future__ import print_function
from constants import column_names
import pandas
import sqlite3
import tornado.web
import random
import sys

data = pandas.read_hdf('../machine/data.h5', 'df')
burgers = data[data.output == 1]
notburgers = data[data.output == 0]

class BurgerHandler(tornado.web.RequestHandler):
        
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
                                            
    def get(self):
        if random.random > 0.5:
            burger = ','.join(burgers.sample().index.values[0])
        else:
            burger = ','.join(notburgers.sample().index.values[0])
        self.write('{ "burger": [%s] }' % burger)
