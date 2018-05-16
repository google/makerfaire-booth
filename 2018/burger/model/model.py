import warnings
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
from sklearn.exceptions import DataConversionWarning
warnings.filterwarnings(action='ignore', category=DeprecationWarning)
column_names = ['layer0', 'layer1', 'layer2', 'layer3', 'layer4', 'layer5']
from one_hot import get_one_hot
enc = get_one_hot()

UNTRAINED_MODEL_FILENAME="../data/clf.pkl"
SPLIT_FILENAME = '../data/split.h5'

burgers = pandas.read_hdf('../data/data.h5', 'df')
classes = numpy.unique(burgers.output.astype(int))

def create_split():
    X = burgers.drop(['output'], axis=1)
    y = burgers['output']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5)
    X_train.join(y_train).to_hdf(SPLIT_FILENAME, 'train', format='fixed')
    X_test.join(y_test).to_hdf(SPLIT_FILENAME, 'test', format='fixed')

def create_classifier():
    clf = MLPClassifier(solver='adam',
                        activation='relu',
                        hidden_layer_sizes=(128,128),
                        verbose=False,
                        max_iter=1000,
                        tol=1e-8,
                        random_state=1)
    return clf

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

class Model:
    def __init__(self):
        self.clf = pickle.load(open(UNTRAINED_MODEL_FILENAME, "rb"))
        train = pandas.read_hdf('../data/split.h5', 'train')
        test = pandas.read_hdf('../data/split.h5', 'test')
        self.X_train = train.drop(['output'], axis=1)
        self.y_train = train['output']
        self.X_test = test.drop(['output'], axis=1)
        self.y_test = test['output']
        self.all_train = self.X_train.join(self.y_train)
        self.X_test_categoricals = self.X_test[column_names]
        self.tX_test_categoricals = enc.fit_transform(self.X_test_categoricals)

        pos_train = self.all_train[self.all_train.output == True]
        neg_train = self.all_train[self.all_train.output == False]
        ratio = 1000
        train = pos_train.append(neg_train.sample(len(pos_train)*ratio))
        for i in range(10):
            one = train.sample(len(train))
            train_X = one.drop(['output'], axis=1)
            train_y = one['output']
            train_X_categoricals = train_X[column_names]
            self.update(train_X_categoricals, train_y)
        print(self.report())
    

    def update(self, X, y):
        X_categoricals = enc.fit_transform(
            X)
        self.clf.partial_fit(X_categoricals,
                             y.astype(int),
                             classes=classes)
    def dump(self):
        pickle.dump(self.clf, open(TRAINED_MODEL_FILENAME, "wb"))

    def report(self):
        prediction = self.clf.predict(self.tX_test_categoricals)
        accuracy = accuracy_score(self.y_test, prediction)
        cf = confusion_matrix(self.y_test, prediction)
        tp, fp, tn, fn = cf[1][1], cf[0][1], cf[0][0], cf[1][0]
        # p, r, f1, s = precision_recall_fscore_support(self.y_test, prediction)
        response = {
            "loss":self.clf.loss_,
            "n_iter":self.clf.n_iter_,
            "accuracy": accuracy,
            # "p": list(p),
            # "r": list(r),
            "tp": int(tp),
            "fp": int(fp),
            "tn": int(tn),
            "fn": int(fn)
        }
        return response
        # self.write(json.dumps(response))

if __name__ == '__main__':
    if not os.path.exists(UNTRAINED_MODEL_FILENAME):
        if os.path.exists(SPLIT_FILENAME):
            os.remove(SPLIT_FILENAME)
        create_split()
        clf = create_classifier()
        pickle.dump(clf, open(UNTRAINED_MODEL_FILENAME, "wb"))
        
    m = Model()

    while True:
        burger = m.all_train.sample(1000)
        m.update(burger[column_names], burger['output'].astype('int'))
        print(m.report())

    # print(m.report())
    # m.update(numpy.array([[1,2,3,4,5,6]]), numpy.array([1]))
    # print(m.report())
    # m.update(numpy.array([[6,6,6,6,6,6]]), numpy.array([0]))
