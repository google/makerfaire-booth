from __future__ import print_function
from constants import column_names
import pandas
import sqlite3
import tornado.web
import random
import sys


class BurgerHandler(tornado.web.RequestHandler):
    def initialize(self, connection):
        self.connection = connection
        self.all = pandas.read_sql_query('SELECT layers.burger, labels.output, layers.layer0, layers.layer1, layers.layer2, layers.layer3, layers.layer4, layers.layer5 FROM layers, labels WHERE layers.burger = labels.burger', self.connection, index_col='burger')
        self.burgers = self.all[self.all.output == 1]
        self.notburgers = self.all[self.all.output == 0]
        
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
                                            
    def get(self):
        if random.random > 0.5:
            burger = ','.join(self.burgers.sample().index.values[0])
        else:
            burger = ','.join(self.notburgers.sample().index.values[0])
        self.write('{ "burger": [%s] }' % burger)
