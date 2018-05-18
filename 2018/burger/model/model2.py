import sqlite3                           
import tempfile
import warnings
import time
import random
import numpy
import pandas
import os
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.exceptions import DataConversionWarning
warnings.filterwarnings(action='ignore', category=DeprecationWarning)
column_names = ['layer0', 'layer1', 'layer2', 'layer3', 'layer4', 'layer5']
import sys
sys.path.insert(0, '../constants')
from one_hot import get_one_hot
enc = get_one_hot()


burgers = pandas.read_hdf('../data/data.h5', 'df')
pos = burgers[burgers.output == True]
pos_categoricals = enc.fit_transform(pos[column_names])
all_categoricals = enc.fit_transform(burgers[column_names])


class Model:
    def __init__(self):
        self.connection = sqlite3.connect('../data/server.db')
        self.clf = None
        
    def update(self):
        all_ = pandas.read_sql_query('SELECT burger, vote FROM votes', self.connection, index_col='burger')
        if len(all_) == 0:
            return 0
            
        X = [[int(item) for item in list(value)] for value in all_.index.values]
        X_categoricals = enc.fit_transform(X)
        y = all_['vote']
        self.clf = MLPClassifier(solver='adam',
                                 activation='relu',
                                 hidden_layer_sizes=(8,8),
                                 verbose=False,
                                 max_iter=1000,
                                 tol=1e-8,
                                 random_state=1)
        self.clf.fit(X_categoricals,y.astype(int))
        return len(all_)

    def label(self, burger):
        n_votes = self.update()
        if n_votes == 0:
            return None
        if self.clf is None:
            return None
        categoricals = enc.fit_transform([burger])
        prediction = self.clf.predict(categoricals)
        return prediction

    def rank(self):
        n_votes = self.update()
        if n_votes == 0:
            return None
        if self.clf is None:
            return None
        all_p = self.clf.predict_proba(all_categoricals)
        prediction = all_p[:,1] > 0.5
        cf = confusion_matrix(burgers.output.astype(int), prediction.astype(int))
        tp, fp, tn, fn = cf[1][1], cf[0][1], cf[0][0], cf[1][0]

        predicted_burgers = pandas.DataFrame(data={'p_burger': all_p[:,1], 'output': burgers.output}, index=burgers.index)
        burgerrank = predicted_burgers[predicted_burgers.p_burger > 0.5].sort_values(by='p_burger', ascending=False).head(10)
        return burgerrank, tp, fp, tn, fn, n_votes
        
if __name__ == '__main__':
    m = Model()
    while True:
        df = m.update()
        print m.rank()
