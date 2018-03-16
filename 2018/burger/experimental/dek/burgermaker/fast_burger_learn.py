import graphviz
import cPickle as pickle
import collections
import operator
import pandas
import itertools
from scipy.sparse import csr_matrix, hstack
from sklearn.svm import SVC
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier, export_graphviz
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

def index_to_burger(index):
    return [int(layer) for layer in list(index)]

def has_sequential_nonempty_duplicates(burger):
  for i in range(len(burger)-1):
    first, second = burger[i], burger[i+1]
    if first != BurgerElement.empty.value and second != BurgerElement.empty.value and first == second:
      return False
  return True

# def get_crown_pos(burger):
#   crown_pos = None
#   for i in range(len(burger)):
#     layer = burger[i]
#     # base case
#     if layer == BurgerElement.empty.value:
#       continue
#     if layer == BurgerElement.crown.value:
#       crown_pos = i
#       break
#     break
#   return crown_pos

def has_internal_or_terminal_empty(burger):
  i = 0
  # Consume initial empties
  while i < 8:
    if burger[i] != BurgerElement.empty.value:
      break
    i += 1
    
  # Consume subsequent non-empties
  while i < 8:
    if burger[i] == BurgerElement.empty.value:
      return True
    i += 1
    
  return False

def has_internal_bun(burger):
  i = 0
  # Consume initial crown
  while i < 7:
    if burger[i] == BurgerElement.crown.value:
      break
    i += 1

  if i == 7:
    return False

  while i < 7:
    if burger[i] == BurgerElement.crown.value or burger[i] == BurgerElement.heel.value:
      return True
    i += 1

  return False


def empty_prefix_count(burger):
  i = 0
  while i < 8:
    if burger[i] != BurgerElement.empty.value:
      break
    i += 1
  return i

def empty_crown_prefix(burger):
  i = 0
  while i < 8:
    if burger[i] == BurgerElement.empty.value:
      i += 1
      continue
    if burger[i] == BurgerElement.crown.value:
      break
    return False
  return True

def has_patty_under_last_cheese(burger):
  last_cheese = None
  for i in range(len(burger)):
    if burger[i] == BurgerElement.cheese.value:
      last_cheese = i
  if last_cheese is None:
    return True
  for i in range(last_cheese+1, len(burger)):
    if burger[i] == BurgerElement.patty.value:
      return True
  return False

  
def count(burger):
  c = collections.Counter(burger)
  return c

def crown_count(burger):
  count = 0
  for i in range(len(burger)):
    if burger[i] == BurgerElement.crown.value:
      count += 1
  return count
def heel_count(burger):
  count = 0
  for i in range(len(burger)):
    if burger[i] == BurgerElement.heel.value:
      count += 1
  return count

#   # import pdb; pdb.set_trace()
#   i = 0
#   # Consume initial empties
#   while i < 8:
#     if burger[i] != BurgerElement.empty.value:
#       break
#     i += 1

#   if i == 8:
#     return False
  
#   # Consume subsequent crown
#   if burger[i] != BurgerElement.crown.value:
#     return False
#   crown_pos = i
  
#   for i in range(crown_pos+1, len(burger)):
#     if burger[i] == BurgerElement.crown.value:
#       return True
    
#   return False

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


names = [member.name for member in BurgerElement.__members__.values()]
# values = [member.value for member in BurgerElement.__members__.values()]
# burgers_it = itertools.product(values, repeat=8)
# burgers = list(burgers_it)
# index = [burger_to_index(burger) for burger in burgers]
# df = pandas.DataFrame(data=burgers,
#                       columns = ['layer0', 'layer1', 'layer2', 'layer3', 'layer4', 'layer5', 'layer6', 'layer7'],
#                       index=index)

# labels = [label_burger(burger) for burger in burgers]
# df['output'] = labels
# # df.to_csv('data.csv', index_label='id')

# count = dict([(burger, count(burger)) for burger in burgers])
# crown_getter = operator.itemgetter(BurgerElement.crown.value)
# heel_getter = operator.itemgetter(BurgerElement.heel.value)
# patty_getter = operator.itemgetter(BurgerElement.patty.value)
# df['has_sequential_nonempty_duplicates'] = [has_sequential_nonempty_duplicates(burger) for burger in burgers]
# df['has_internal_or_terminal_empty'] = [has_internal_or_terminal_empty(burger) for burger in burgers]
# df['has_patty_under_last_cheese'] = [has_patty_under_last_cheese(burger) for burger in burgers]
# df['has_internal_bun'] = [has_internal_bun(burger) for burger in burgers]
# df['empty_prefix_count'] = [empty_prefix_count(burger) for burger in burgers]
# df['empty_crown_prefix'] = [empty_crown_prefix(burger) for burger in burgers]
# df['crown_count'] = [crown_getter(count[burger]) for burger in burgers]
# df['heel_count'] = [heel_getter(count[burger]) for burger in burgers]
# df['patty_count'] = [patty_getter(count[burger]) for burger in burgers]

# df.to_hdf('data.h5', 'df', format='fixed')
df = pandas.read_hdf('data.h5', 'df')

pos = df[df.output == True]
neg = df[df.output == False]
neg_sampled = neg.sample(len(pos)*1000)
dataset = pos.append(neg_sampled)
X = dataset.drop(['output'], axis=1)
y = dataset['output']

X_train, X_test, y_train, y_test = train_test_split(X, y)

enc = OneHotEncoder()
X_train_categoricals = X_train[['layer0','layer1','layer2','layer3','layer4','layer5','layer6','layer7']]
tX_train_categoricals = enc.fit_transform(X_train_categoricals)
m = csr_matrix([
  X_train['has_sequential_nonempty_duplicates'].astype(int),
  X_train['has_internal_or_terminal_empty'].astype(int),
  X_train['has_patty_under_last_cheese'].astype(int),
  X_train['has_internal_bun'].astype(int),
  X_train['empty_prefix_count'],
  X_train['empty_crown_prefix'],
  X_train['crown_count'],
  X_train['heel_count'],
  X_train['patty_count']
])
all_X_train= hstack([tX_train_categoricals, m.T])
# all_X_train = m.T
# # all_X_train= tX_train_categoricals

# # # clf = SVC(gamma=0.001, C=1., verbose=True)
# # # clf = RandomForestClassifier(n_estimators=100, n_jobs=8, max_features=3,
# # #                              max_depth=None, random_state=0, verbose=True)
# # clf = MLPClassifier(solver='adam',  activation='identity',
# #                     hidden_layer_sizes=(1,), verbose=True)

# clf = DecisionTreeClassifier(random_state=0, class_weight="balanced", max_depth=None)

# clf = BaggingClassifier(KNeighborsClassifier(), max_samples=0.5, max_features=0.5, n_jobs=8, verbose=True)
# clf = AdaBoostClassifier(n_estimators=100)
clf = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0,
                                 max_depth=1)
# print "Training"
clf.fit(all_X_train, y_train.as_matrix().astype(int))
# pickle.dump(clf, open("mlp.pkl", "w"))
# clf = pickle.load(open("mlp.pkl"))


# feature_names = []
# for name in ['layer0','layer1','layer2','layer3','layer4','layer5','layer6','layer7']:
#   for i in range(len(names)):
#     feature_names.append(name + "_" + names[i])
# feature_names.append('has_sequential_nonempty_duplicates')
# feature_names.append('has_internal_or_terminal_empty')
# feature_names.append('has_patty_under_last_cheese')
# feature_names.append('has_internal_bin')
# feature_names.append('empty_prefix_count')
# feature_names.append('empty_crown_count')
# feature_names.append('crown_count')
# feature_names.append('heel_crown_count')
# feature_names.append('patty_count')
#dot_data = export_graphviz(clf, out_file="test.dot", feature_names=feature_names)

X_test_categoricals = X_test[['layer0','layer1','layer2','layer3','layer4','layer5','layer6','layer7']]
tX_test_categoricals = enc.fit_transform(X_test_categoricals)
m = csr_matrix([
  X_test['has_sequential_nonempty_duplicates'].astype(int),
  X_test['has_internal_or_terminal_empty'].astype(int),
  X_test['has_patty_under_last_cheese'].astype(int),
  X_test['has_internal_bun'].astype(int),
  X_test['empty_prefix_count'],
  X_test['empty_crown_prefix'],
  X_test['crown_count'],
  X_test['heel_count'],
  X_test['patty_count']
])
all_X_test= hstack([tX_test_categoricals, m.T])
# all_X_test = m.T
# all_X_test= tX_test_categoricals

prediction = clf.predict(all_X_test)
print accuracy_score(y_test, prediction)
cf = confusion_matrix(y_test, prediction)

print "TP:", cf[1][1]
print "FP:", cf[0][1]
print "TN:", cf[0][0]
print "FN:", cf[1][0]


X = df.drop(['output'], axis=1)
y = df['output']
X_categoricals = X[['layer0','layer1','layer2','layer3','layer4','layer5','layer6','layer7']]
tX_categoricals = enc.fit_transform(X_categoricals)
m = csr_matrix([
  X['has_sequential_nonempty_duplicates'].astype(int),
  X['has_internal_or_terminal_empty'].astype(int),
  X['has_patty_under_last_cheese'].astype(int),
  X['has_internal_bun'].astype(int),
  X['empty_prefix_count'],
  X['empty_crown_prefix'],
  X['crown_count'],
  X['heel_count'],
  X['patty_count']
])
all_X= hstack([tX_categoricals, m.T])
# all_X = m.T
# all_X= tX_categoricals

prediction = clf.predict(all_X)
print accuracy_score(y, prediction)
cf = confusion_matrix(y, prediction)

print "TP:", cf[1][1]
print "FP:", cf[0][1]
print "TN:", cf[0][0]
print "FN:", cf[1][0]

df['prediction'] = prediction.astype(bool)


fp = df[~df.output & df.prediction]
for index, row in fp.iterrows():
    print index
    label_burger([int(layer) for layer in index], True)
