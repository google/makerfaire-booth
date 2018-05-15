from __future__ import print_function
import sys
sys.path.insert(0, "../constants")
from constants import column_names
import tornado.web
import random

class BurgerHandler(tornado.web.RequestHandler):
    def initialize(self, burgers):
        self.burgers = burgers[burgers.output == 1]
        self.notburgers = burgers[burgers.output == 0]

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
                                            
    def get(self):
        is_burger = None
        if random.random() > 0.5:
            is_burger = True
            burger = ','.join(self.burgers.sample().index.values[0])
        else:
            is_burger = False
            burger = ','.join(self.notburgers.sample().index.values[0])
        true_label = str(is_burger).lower()
        self.write('{ "burger": [%s], "true_label": %s }' % (burger, true_label))
