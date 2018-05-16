from __future__ import print_function
import numpy
import sys
sys.path.insert(0,'../constants')
from constants import column_names
from one_hot import get_one_hot
import tornado.web
import random
import pickle
enc = get_one_hot()

class RankHandler(tornado.web.RequestHandler):
    def initialize(self, burgers):
        self.burgers = burgers

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
                                            
    def get(self):
        clf = pickle.load(open("../data/trained.pkl", "rb"))
        s = [list(item) for item in self.burgers.index.values]
        ts = enc.fit_transform(s)
        p = clf.predict_proba(ts)
        self.burgers['p_burger'] = p[:,1]
        import pdb; pdb.set_trace()

