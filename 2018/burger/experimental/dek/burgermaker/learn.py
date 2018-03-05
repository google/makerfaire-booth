import sys
import numpy
import itertools
import pickle
import random
from sklearn import svm
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

o = open("dataset.pkl")
X = pickle.load(o)
y = pickle.load(o)
o.close()

new_X = []
new_y = []
for i in range(len(X)):
  if y[i] == True:
    new_X.append(X[i])
    new_y.append(True)
  else:
    if random.random() < 1/100.:
      new_X.append(X[i])
      new_y.append(False)

o = open("mini_dataset.pkl", "w")
pickle.dump(new_X, o)
pickle.dump(new_y, o)
o.close()

# o = open("mini_dataset.pkl")
# X = pickle.load(o)
# y = pickle.load(o)
# o.close()


# print "# of y:", len(y)
# print "# true:", len([item for item in y if item is True])

# print "data loaded"
# X = numpy.array(X)
# y = numpy.array(y)

# clf = svm.SVC()
# clf.fit(X, y)

# test_cases = itertools.product( [BurgerElement.empty, BurgerElement.crown, BurgerElement.lettuce, BurgerElement.tomato, BurgerElement.cheese, BurgerElement.patty, BurgerElement.heel], repeat=8)

# tp = 0
# tn = 0
# fp = 0
# fn = 0
# for test in test_cases:
#   v = [layer.value for layer in test]
#   t = numpy.array(v).reshape(1, -1)
#   # TODO: run prediction on BurgerElement values
#   # TODO: run check_burger on BurgerElements
#   prediction = clf.predict(t)[0]
#   label = check_burger(test)
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
