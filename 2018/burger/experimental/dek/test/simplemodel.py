from __future__ import print_function
import pickle
import pandas
import numpy
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score, confusion_matrix, roc_curve, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
column_names = ['layer0', 'layer1', 'layer2', 'layer3', 'layer4', 'layer5']
import sqlite3

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

def main():
    enc = OneHotEncoder(n_values=[7,7,7,7,7,7])
    conn = sqlite3.connect('server.db')
    cursor = conn.cursor()
    all_ = pandas.read_sql_query('SELECT layers.burger, labels.output, layers.layer0, layers.layer1, layers.layer2, layers.layer3, layers.layer4, layers.layer5 FROM layers,labels WHERE layers.burger = labels.burger', conn, index_col='burger')
    
    X = all_.drop(['output'], axis=1)
    y = all_['output']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5)

               
    clf = MLPClassifier(solver='adam',  activation='relu',
                        verbose=False,
                        max_iter=10000,
                        tol=1e-9,
                        random_state=1)
    
    X_train_categoricals = X_train[column_names]
    tX_train_categoricals = enc.fit_transform(X_train_categoricals)
    clf.fit(tX_train_categoricals, y_train.as_matrix().astype(int))

    
    X_test_categoricals = X_test[column_names]
    tX_test_categoricals = enc.fit_transform(X_test_categoricals)
    prediction = clf.predict(tX_test_categoricals)
    
    print(classification_report(y_test, prediction))
    
    print_eval(y_test, prediction)

if __name__ == '__main__':
    main()
