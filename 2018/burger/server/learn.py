from __future__ import print_function
import os
import time
import pickle
import pandas
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from constants import MAX_BURGER_HEIGHT, column_names
import sqlite3

# df = pandas.read_hdf('data.h5', 'df')
# pos = df[df.output == True]
# neg = df[df.output == False]
# dataset = pos.append(neg)
# X = dataset.drop(['output'], axis=1)
# y = dataset['output']
conn = sqlite3.connect('server.db')

while True:
    data = pandas.read_sql_query('SELECT layers.burger, votes.vote, layers.layer0, layers.layer1, layers.layer2, layers.layer3, layers.layer4, layers.layer5 FROM layers, votes WHERE layers.burger = votes.burger', conn, index_col='burger')
    X = data.drop(['vote'], axis=1)
    if len(X) == 0:
        print("Waiting on votes")
        time.sleep(10)
        continue
    print("Training on", len(X))
        
    y = data['vote']
    enc = OneHotEncoder(n_values=[7,7,7,7,7,7])
    X_categoricals = X[column_names]
    tX_categoricals = enc.fit_transform(X_categoricals)
    clf = MLPClassifier(solver='adam',  activation='relu',
                        hidden_layer_sizes=(32,32), verbose=False, max_iter=10000, tol=1e-9, random_state=1)
    clf.fit(tX_categoricals, y.as_matrix().astype(int))

    all_ = pandas.read_sql_query('SELECT layers.burger, labels.output, layers.layer0, layers.layer1, layers.layer2, layers.layer3, layers.layer4, layers.layer5 FROM layers, labels WHERE layers.burger = labels.burger', conn, index_col='burger')
    X = all_.drop(['output'], axis=1)
    y = all_['output']
    X_categoricals = X[column_names]
    tX_categoricals = enc.fit_transform(X_categoricals)
    prediction = clf.predict(tX_categoricals)
    all_['prediction'] = prediction
    print("All:")
    print(accuracy_score(y, prediction))
    cf = confusion_matrix(y, prediction)

    print("TP:", cf[1][1])
    print("FP:", cf[0][1])
    print("TN:", cf[0][0])
    print("FN:", cf[1][0])

    probs = clf.predict_proba(tX_categoricals)
    all_['prob'] = probs[:, 0]
    sorted_all = all_.sort_values('prob', axis=0)

