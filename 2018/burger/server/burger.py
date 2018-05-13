from __future__ import print_function
import sys
sys.path.insert(0, "../constants")
from constants import column_names
import pandas
import tornado.web
import random

data = pandas.read_hdf('split.h5', 'train')
burgers = data[data.output == 1]
notburgers = data[data.output == 0]

class BurgerHandler(tornado.web.RequestHandler):
        
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
                                            
    def get(self):
        is_burger = None
        if random.random() > 0.5:
            is_burger = True
            burger = ','.join(burgers.sample().index.values[0])
        else:
            is_burger = False
            burger = ','.join(notburgers.sample().index.values[0])
        true_label = str(is_burger).lower()
        self.write('{ "burger": [%s], "true_label": %s }' % (burger, true_label))
