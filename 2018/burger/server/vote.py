import json
import tornado.web
import numpy
import sqlite3
import pandas
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

column_names = ['layer0', 'layer1', 'layer2', 'layer3', 'layer4', 'layer5']
burgers = pandas.read_hdf('../machine/data.h5', 'df')
enc = OneHotEncoder(n_values=[7,7,7,7,7,7])

connection = sqlite3.connect('server.db')

X = burgers.drop(['output'], axis=1)
y = burgers['output']
X_categoricals = X[column_names]
tX_categoricals = enc.fit_transform(X_categoricals)

clf = MLPClassifier(solver='adam',  activation='relu',
                    hidden_layer_sizes=64,
                    verbose=False,
                    max_iter=10000,
                    tol=1e-9,
                    random_state=1)

classes = numpy.unique(y.astype(int))

def print_eval(y, prediction):
    print(accuracy_score(y, prediction))
    cf = confusion_matrix(y, prediction)

    tp, fp, tn, fn = cf[1][1], cf[0][1], cf[0][0], cf[1][0]
    print("TP:", tp)
    print("FP:", fp)
    print("TN:", tn)
    print("FN:", fn)
    print("FPR:", fp/float(fp+tn))
    print("FNR:", fn/float(fn+tp))

    return tp, fp, tn, fn


class VoteHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
                                            
    def get(self):
        burger = self.get_argument('burger', '000000')
        vote = bool(self.get_argument('vote', 'true') == 'true')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO votes VALUES (?, ?)", (burger, vote))
        connection.commit()

        burger_df = burgers.loc[burger]
        print(burger)
        sample_X_train = burger_df.drop(["output"])
        sample_y_train = burger_df["output"]
        sample_X_train_categoricals = sample_X_train[column_names]
        sample_tX_train_categoricals = enc.fit_transform(
            sample_X_train_categoricals.values.reshape(1, -1))
        clf.partial_fit(sample_tX_train_categoricals,
                        [int(sample_y_train)],
                        classes=classes)

        prediction = clf.predict(tX_categoricals)
        tp, fp, tn, fn = print_eval(y, prediction)
        report = classification_report(y, prediction)

        user_label = str(vote).lower()
        true_label = str(burger_df['output']).lower()
        response = {
            "burger": burger,
            "user_label": user_label,
            "true_label": true_label,
            "classification_report": report,
            "tp": tp,
            "fp": fp,
            "tn": tn,
            "fn": fn
            }
        self.write(json.dumps(response))



