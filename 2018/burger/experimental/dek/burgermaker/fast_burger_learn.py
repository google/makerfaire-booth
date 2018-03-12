import cPickle as pickle
import pandas
import itertools
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from enum import Enum, unique

@unique
class BurgerElement(Enum):
  empty = 0
  crown = 1
  lettuce = 2
  tomato = 3
  cheese = 4
  patty = 5
  heel = 6

def burger_to_index(burger):
    return ''.join([str(layer) for layer in burger])

def label_burger(burger, debug=False):
  if len(burger) != 8:
    if debug: print "Burger is wrong size"
    return False
  crown_pos = None
  for i in range(len(burger)):
    layer = burger[i]
    # base case
    if layer == BurgerElement.empty.value:
      continue
    if layer == BurgerElement.crown.value:
      crown_pos = i
      break
    if debug: print "prefix elements must be empty or crown"
    return False
  if crown_pos is None:
    if debug: print "Burger does not have crown"
    return False
  if burger[-1] != BurgerElement.heel.value:
    if debug: print "Burger does not have heel bottom"
    return False
  for i in range(crown_pos+1, len(burger)-1):
    if burger[i] == BurgerElement.crown.value or burger[i] == BurgerElement.heel.value:
      if debug: print "Cannot have internal buns"
      return False
  for i in range(crown_pos+1, len(burger)):
    if burger[i] == BurgerElement.empty.value:
      if debug: print "Cannot have internal or terminal empty"
      return False
  for i in range(len(burger)-1):
    first, second = burger[i], burger[i+1]
    if first != BurgerElement.empty.value and second != BurgerElement.empty.value and first == second:
      if debug: print "Cannot have identical sequential items"
      return False
  for i in range(1, len(burger)-1):
    if burger[i] == BurgerElement.patty.value:
      break
  else:
    if debug: print "Must have at least one patty"
    return False
  last_cheese_index = None
  for i in range(1, len(burger)-1):
    if burger[i] == BurgerElement.cheese.value:
      last_cheese_index = i
  if last_cheese_index is not None:
    for i in range(last_cheese_index+1, len(burger)):
      if burger[i] == BurgerElement.patty.value:
        break
    else:
      if debug: print "Must have at patty under last cheese."
      return False


  return True

values = [member.value for member in BurgerElement.__members__.values()]
burgers_it = itertools.product(values, repeat=8)
burgers = list(burgers_it)
labels = [label_burger(burger) for burger in burgers]
index = [burger_to_index(burger) for burger in burgers]
df = pandas.DataFrame(data=burgers, index=index)
df['label'] = labels
df.to_hdf('data.h5', 'df', format='fixed')

pos = df[df.label == True]
neg = df[df.label == False]
neg_sampled = neg.sample(len(pos)*500)
dataset = pos.append(neg_sampled)
X = dataset.drop(['label'], axis=1)
y = dataset['label']

X_train, X_test, y_train, y_test = train_test_split(X, y)

enc = OneHotEncoder()
tX_train = enc.fit_transform(X_train)

clf = MLPClassifier(solver='lbfgs', alpha=1e-5, tol=1e-5,
                    hidden_layer_sizes=(64, 64), random_state=1, verbose=True)

clf.fit(tX_train, y_train.as_matrix().astype(int))
pickle.dump(clf, open("mlp.pkl", "w"))
clf = pickle.load(open("mlp.pkl"))

tX_test = enc.fit_transform(X_test)
prediction = clf.predict(tX_test)
print accuracy_score(y_test, prediction)
cf = confusion_matrix(y_test, prediction)

print "TP:", cf[1][1]
print "FP:", cf[0][1]
print "TN:", cf[0][0]
print "FN:", cf[1][0]


X = df.drop(['label'], axis=1)
y = df['label']
tX = enc.fit_transform(X)
prediction = clf.predict(tX)
print accuracy_score(y, prediction)
cf = confusion_matrix(y, prediction)

print "TP:", cf[1][1]
print "FP:", cf[0][1]
print "TN:", cf[0][0]
print "FN:", cf[1][0]

df['prediction'] = prediction.astype(bool)


fp = df[~df.label & df.prediction]
for index, row in fp.iterrows():
    print index
    label_burger([int(layer) for layer in index], True)

# df.to_csv("predictions.csv")
    
