import pandas
import sys
import numpy
import itertools
import pickle
import random
import numpy as np
from sklearn import svm
from sklearn import linear_model
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
import csv

import sys
sys.path.insert(0, "../burgerdata")
from burger_data import BurgerElement
from burger_checker import check_burger

# TODO(dek): move this into burger_generator

data = pandas.read_csv("burgers.csv")
y = data['label']
pos = data[data.label == True]
neg = data[data.label == False]
neg_sampled = data.sample(len(pos)*500)
dataset = pos.append(neg_sampled)
X = dataset.drop(['label'], axis=1)
y = dataset['label']

X_train, X_test, y_train, y_test = train_test_split(X, y)

enc = OneHotEncoder()
tX_train = enc.fit_transform(X_train)

clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                    hidden_layer_sizes=(8, 2), random_state=1)

clf.fit(tX_train, y_train.as_matrix().astype(int))

tX_test = enc.fit_transform(X_test)
prediction = clf.predict(tX_test)
print accuracy_score(y_test, prediction)
cf = confusion_matrix(y_test, prediction)

print "TP:", cf[1][1]
print "FP:", cf[0][1]
print "TN:", cf[0][0]
print "FN:", cf[1][0]


X = data.drop(['label'], axis=1)
y = data['label']
tX = enc.fit_transform(X)
prediction = clf.predict(tX)
print accuracy_score(y, prediction)
cf = confusion_matrix(y, prediction)

print "TP:", cf[1][1]
print "FP:", cf[0][1]
print "TN:", cf[0][0]
print "FN:", cf[1][0]

data['prediction'] = prediction.astype(bool)

data.to_csv("predictions.csv")
    
