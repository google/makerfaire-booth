import pickle
import json
import tornado.web
import numpy
import pandas
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import model
from one_hot import get_one_hot
enc = get_one_hot()

column_names = ['layer0', 'layer1', 'layer2', 'layer3', 'layer4', 'layer5']
burgers = pandas.read_hdf('split.h5', 'train')
X_train = burgers.drop(['output'], axis=1)
y_train = burgers['output']
classes = numpy.unique(y_train)

class VoteHandler(tornado.web.RequestHandler):
    def initialize(self, burgers, connection):
        self.burgers = burgers
        self.connection = connection

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
                                            
    def get(self):
        burger = self.get_argument('burger')
        vote_arg = self.get_argument('vote')
        vote = vote_arg == 'true' or vote_arg == 'True'

        self.connection.cursor().execute("INSERT INTO votes VALUES (?, ?)", (burger, vote))
        self.connection.commit()
        
        try:
            burger_df = burgers.loc[str(burger)]
        except KeyError:
            self.send_error(404)
            return
        

        self.write('{ "burger": "%s", "vote": %s, "label": %s }' %
                   (burger, "true" if vote else "false", burgers.loc[burger].output))

