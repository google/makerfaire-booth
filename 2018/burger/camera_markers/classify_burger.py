from sklearn.preprocessing import OneHotEncoder
import numpy as np
import pickle
import os

class BurgerClassifier(object):
    def __init__(self):
        self.clf = pickle.load(open("../experimental/dek/test/clf.pkl", "rb"))
        self.enc = OneHotEncoder(n_values=[7,7,7,7,7,7])
        
    def classify(self, layers):
        t = np.array(layers).reshape(1, -1)
        tX_train_categoricals = self.enc.fit_transform(t)
        prediction = self.clf.predict_proba(tX_train_categoricals)
        return prediction

if __name__ == '__main__':
    b = BurgerClassifier()
    print(b.classify([1,2,3,4,5,6]))
