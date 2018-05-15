import time
import random
import numpy
import pickle
import pandas
import os
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, precision_recall_fscore_support
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
column_names = ['layer0', 'layer1', 'layer2', 'layer3', 'layer4', 'layer5']
from one_hot import get_one_hot
enc = get_one_hot()

MODEL_FILENAME="../data/clf.pkl"
SPLIT_FILENAME = '../data/split.h5'
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

def setup():
    burgers = pandas.read_hdf('../data/data.h5', 'df')
    X = burgers.drop(['output'], axis=1)
    y = burgers['output']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5)
    X_train.join(y_train).to_hdf(filename, 'train', format='fixed')
    X_test.join(y_test).to_hdf(filename, 'test', format='fixed')

    clf = MLPClassifier(solver='adam',
                        activation='relu',
                        hidden_layer_sizes=(128,128),
                        verbose=True,
                        max_iter=1000,
                        tol=1e-8,
                        random_state=1)
    pickle.dump(clf, open(MODEL_FILENAME, "wb"))

def update(clf):
    sample_X_train = burger_df.drop(["output"])
    sample_y_train = burger_df["output"]
    sample_X_train_categoricals = sample_X_train[column_names]
    sample_tX_train_categoricals = enc.fit_transform(
        sample_X_train_categoricals.values.reshape(1, -1))
    clf.partial_fit(sample_tX_train_categoricals,
                         [int(sample_y_train)],
                         classes=classes)
    pickle.dump(clf, open(MODEL_FILENAME, "wb"))

def report(clf):
    X_test_categoricals = self.X_test[column_names]
    tX_test_categoricals = enc.fit_transform(X_test_categoricals)
    prediction = clf.predict(tX_test_categoricals)
    accuracy = accuracy_score(self.y_test, prediction)
    cf = confusion_matrix(self.y_test, prediction)
    tp, fp, tn, fn = cf[1][1], cf[0][1], cf[0][0], cf[1][0]
    p, r, f1, s = precision_recall_fscore_support(self.y_test, prediction)
    response = {
        "loss":clf.loss_,
        "n_iter":clf.n_iter_,
        "accuracy": accuracy,
        "p": list(p),
        "r": list(r),
        "tp": int(tp),
        "fp": int(fp),
        "tn": int(tn),
        "fn": int(fn)
    }
    self.write(json.dumps(response))

if __name__ == '__main__':
    if not os.path.exists(MODEL_FILENAME):
        if os.path.exists(SPLIT_FILENAME):
            os.remove(SPLIT_FILENAME)
        setup()
