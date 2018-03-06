import sys
import numpy
import itertools
import pickle
import random
from sklearn import svm
from sklearn.preprocessing import OneHotEncoder
import csv

import sys
sys.path.insert(0, "../burgerdata")
from burger_data import BurgerElement
from burger_checker import check_burger

# TODO(dek): move this into burger_generator

# X = []
# y = []
# all_burgers_labelled = pickle.load(open("burgers.pkl"))
# for burger in all_burgers_labelled:
#   v = [layer.value for layer in burger]
#   X.append(v)
#   y.append(all_burgers_labelled[burger])
# o = open("dataset.pkl", "w")
# pickle.dump(X, o)
# pickle.dump(y, o)
# o.close()

# o = open("dataset.pkl")
# X = pickle.load(o)
# y = pickle.load(o)
# o.close()

# new_X = []
# new_y = []
# for i in range(len(X)):
#   if y[i] == True:
#     new_X.append(X[i])
#     new_y.append(True)
#   else:
#     if random.random() < 1/100.:
#       new_X.append(X[i])
#       new_y.append(False)

# o = open("mini_dataset.pkl", "w")
# pickle.dump(new_X, o)
# pickle.dump(new_y, o)
# o.close()

o = open("mini_dataset.pkl")
X = pickle.load(o)
y = pickle.load(o)
o.close()

enc = OneHotEncoder()
tX = enc.fit_transform(X)

print "# of y:", len(y)
print "# true:", len([item for item in y if item is True])

print "data loaded"
X = numpy.array(X)
y = numpy.array(y)

clf = svm.SVC()
clf.fit(tX, y)

# test_cases = itertools.product( [BurgerElement.empty, BurgerElement.crown, BurgerElement.lettuce, BurgerElement.tomato, BurgerElement.cheese, BurgerElement.patty, BurgerElement.heel], repeat=8)
test_cases2 = itertools.product( [BurgerElement.empty.value, BurgerElement.crown.value, BurgerElement.lettuce.value, BurgerElement.tomato.value, BurgerElement.cheese.value, BurgerElement.patty.value, BurgerElement.heel.value], repeat=8)
l = list(test_cases2)
tl = enc.transform(l)
prediction = clf.predict(tl)
# tp = 0
# tn = 0
# fp = 0
# fn = 0
# for i, test in enumerate(test_cases):
  # v = [item.value for item in test]
  # t = numpy.array(test_cases2[i]).reshape(1, -1)
#   prediction = clf.predict(enc.transform(t))[0]
#   label = check_burger(test)
#   print t, prediction, label
#   if prediction == True:
#     if prediction == label:
#       tp += 1
#     else:
#       fp += 1
#   else:
#     if prediction == label:
#       tn += 1
#     else:
#       fn += 1

# print tp, fp, tn, fn
