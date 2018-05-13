from __future__ import print_function
import os
import pickle
import pandas
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
import sys
sys.path.insert(0, "../constants")
from constants import MAX_BURGER_HEIGHT, column_names

df = pandas.read_hdf('data.h5', 'df')
pos = df[df.output == True]
neg = df[df.output == False]
dataset = pos.append(neg)
X = dataset.drop(['output'], axis=1)
y = dataset['output']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

enc = OneHotEncoder()
X_train_categoricals = X_train[column_names]
tX_train_categoricals = enc.fit_transform(X_train_categoricals)
all_X_train= tX_train_categoricals

clf = MLPClassifier(solver='adam',  activation='relu',
                    hidden_layer_sizes=(32,32), verbose=False, max_iter=10000, tol=1e-9)
clf.fit(all_X_train, y_train.as_matrix().astype(int))
pickle.dump(clf, open("mlp.pkl", "wb"))
clf = pickle.load(open("mlp.pkl", "rb"))

X_test_categoricals = X_test[column_names]
tX_test_categoricals = enc.fit_transform(X_test_categoricals)
all_X_test= tX_test_categoricals

prediction = clf.predict(all_X_test)
print("Test set:")
print(accuracy_score(y_test, prediction))
cf = confusion_matrix(y_test, prediction)

print("TP:", cf[1][1])
print("FP:", cf[0][1])
print("TN:", cf[0][0])
print("FN:", cf[1][0])


X = df.drop(['output'], axis=1)
y = df['output']
X_categoricals = X[column_names]
tX_categoricals = enc.fit_transform(X_categoricals)
all_X= tX_categoricals

prediction = clf.predict(all_X)
print("All:")
print(accuracy_score(y, prediction))
cf = confusion_matrix(y, prediction)

print("TP:", cf[1][1])
print("FP:", cf[0][1])
print("TN:", cf[0][0])
print("FN:", cf[1][0])

df['prediction'] = prediction.astype(bool)


fp = df[~df.output & df.prediction]
for index, row in fp.iterrows():
    print("FP:",index)
fn = df[df.output & ~df.prediction]
for index, row in fn.iterrows():
    print("FN:",index)
