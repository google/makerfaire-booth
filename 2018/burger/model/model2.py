import sqlite3                           
import tempfile
import warnings
import time
import random
import numpy
import pandas
import os
from sklearn.neural_network import MLPClassifier
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
            return False
            
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
        return True
    def rank(self):
        if self.update() is False:
            return None
        if self.clf is None:
            return None
        all_p = self.clf.predict_proba(all_categoricals)
        df = pandas.DataFrame(data={'p_burger': all_p[:,1]}, index=burgers.index)
        return df.sort_values(by='p_burger', ascending=False).head(10)
        
if __name__ == '__main__':
    m = Model()
    while True:
        df = m.update()
        print(df.sort_values(by=['p_burger']).tail(10))
