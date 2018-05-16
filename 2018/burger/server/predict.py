from __future__ import print_function
import sys
sys.path.insert(0, "../constants")
from constants import column_names
from one_hot import get_one_hot
import tornado.web
import random
import pickle

enc = get_one_hot()

class PredictHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
                                            
    def get(self):
        clf = pickle.load(open("../data/trained.pkl", "rb"))
        burger = list(self.get_argument('burger'))
        tburger = enc.fit_transform([burger])
        p = clf.predict(burger)
        self.write('{ "prediction": %s }' % p.lower())
