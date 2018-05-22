from sklearn.preprocessing import OneHotEncoder
import numpy as np
import pickle
import os
import sys
sys.path.insert(0, "../constants")
from one_hot import get_one_hot

class BurgerClassifier(object):
    def __init__(self):
        self.clf = pickle.load(open("../data/trained.pkl", "rb"))
        self.enc = get_one_hot()
        
    def classify(self, layers):
        t = np.array(layers).reshape(1, -1)
        tX_train_categoricals = self.enc.fit_transform(t)
        prediction = self.clf.predict_proba(tX_train_categoricals)
        return prediction

if __name__ == '__main__':
    b = BurgerClassifier()
    print(b.classify([1,2,3,4,5,6]))
