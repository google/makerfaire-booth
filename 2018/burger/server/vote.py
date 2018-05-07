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


column_names = ['layer0', 'layer1', 'layer2', 'layer3', 'layer4', 'layer5']
enc = OneHotEncoder(n_values=[7,7,7,7,7,7])
burgers = pandas.read_hdf('split.h5', 'train')
X_train = burgers.drop(['output'], axis=1)
y_train = burgers['output']
classes = numpy.unique(y_train)

class VoteHandler(tornado.web.RequestHandler):
    def initialize(self, clf, burgers):
        self.clf = clf
        self.burgers = burgers

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
                                            
    def get(self):
        burger = self.get_argument('burger')
        vote_arg = self.get_argument('vote')
        vote = vote_arg == 'true' or vote_arg == 'True'
        try:
            burger_df = burgers.loc[str(burger)]
        except KeyError:
            self.send_error(404)
            return
        
        sample_X_train = burger_df.drop(["output"])
        sample_y_train = burger_df["output"]
        sample_X_train_categoricals = sample_X_train[column_names]
        sample_tX_train_categoricals = enc.fit_transform(
            sample_X_train_categoricals.values.reshape(1, -1))
        self.clf.partial_fit(sample_tX_train_categoricals,
                             [int(sample_y_train)],
                             classes=classes)
        pickle.dump(self.clf, open("clf.pkl", "wb"))

        self.write('{ "burger": "%s", "vote": %s, "label": %s }' %
                   (burger, "true" if vote else "false", burgers.loc[burger].output))

