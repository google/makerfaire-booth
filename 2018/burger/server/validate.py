import json
import tornado.web
import pandas
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import precision_recall_fscore_support
import model


column_names = ['layer0', 'layer1', 'layer2', 'layer3', 'layer4', 'layer5']
enc = OneHotEncoder(n_values=[7,7,7,7,7,7])



class ValidateHandler(tornado.web.RequestHandler):
    def initialize(self, clf, burgers):
        self.clf = clf
        self.burgers = burgers
        self.X_test = burgers.drop(['output'], axis=1)
        self.y_test = burgers['output']

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
                                            
    def get(self):
        X_test_categoricals = self.X_test[column_names]
        tX_test_categoricals = enc.fit_transform(X_test_categoricals)
        prediction = self.clf.predict(tX_test_categoricals)
        accuracy = accuracy_score(self.y_test, prediction)
        cf = confusion_matrix(self.y_test, prediction)
        tp, fp, tn, fn = cf[1][1], cf[0][1], cf[0][0], cf[1][0]
        p, r, f1, s = precision_recall_fscore_support(self.y_test, prediction)
        response = {
            "loss":self.clf.loss_,
            "n_iter":self.clf.n_iter_,
            "accuracy": accuracy,
            "p": list(p),
            "r": list(r),
            "tp": int(tp),
            "fp": int(fp),
            "tn": int(tn),
            "fn": int(fn)
            }
        self.write(json.dumps(response))



