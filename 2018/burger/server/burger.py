from __future__ import print_function
from constants import column_names
import pandas
import sqlite3
import tornado.web
import random
from sklearn.preprocessing import OneHotEncoder
import sys
sys.path.insert(0, "../machine")
import label_burger

conn = sqlite3.connect('server.db')
c = conn.cursor()
all_ = pandas.read_sql_query('SELECT layers.burger, labels.output, layers.layer0, layers.layer1, layers.layer2, layers.layer3, layers.layer4, layers.layer5 FROM layers, labels WHERE layers.burger = labels.burger', conn, index_col='burger')

sample=all_[all_.output == 0].sample()[['layer0', 'layer1', 'layer2', 'layer3', 'layer4', 'layer5']].values[0]

class BurgerHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
                                            
    def get(self):
        if random.random > 0.5:
            burger = ','.join(all_[all_.output == 1].sample().index.values[0])
        else:
            burger = ','.join(all_[all_.output == 0].sample().index.values[0])
        self.write('{ "burger": [%s] }' % burger)
