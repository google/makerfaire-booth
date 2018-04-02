import graphviz
import cPickle as pickle
import pandas
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
from constants import MAX_BURGER_HEIGHT, column_names

df = pandas.read_hdf('data.h5', 'df')
pos = df[df.output == True]
neg = df[df.output == False]
neg_sampled = neg.sample(len(pos)*1000)
dataset = pos.append(neg_sampled)
X = dataset.drop(['output'], axis=1)
y = dataset['output']


X_train, X_test, y_train, y_test = train_test_split(X, y)

enc = OneHotEncoder()
X_train_categoricals = X_train[column_names]
tX_train_categoricals = enc.fit_transform(X_train_categoricals)
m = csr_matrix([
  X_train['has_sequential_nonempty_duplicates'].astype(int),
  X_train['has_internal_or_terminal_empty'].astype(int),
  X_train['has_patty_under_last_cheese'].astype(int),
  X_train['has_internal_bun'].astype(int),
  X_train['empty_prefix_count'],
  X_train['empty_topbun_prefix'],
  X_train['topbun_count'],
  X_train['bottombun_count'],
  X_train['patty_count']
])
all_X_train= hstack([tX_train_categoricals, m.T])
# all_X_train = m.T
# # all_X_train= tX_train_categoricals

# # # clf = SVC(gamma=0.001, C=1., verbose=True)
# # # clf = RandomForestClassifier(n_estimators=100, n_jobs=8, max_features=3,
# # #                              max_depth=None, random_state=0, verbose=True)
clf = MLPClassifier(solver='adam',  activation='identity',
                    hidden_layer_sizes=(1,), verbose=True)

# clf = DecisionTreeClassifier(random_state=0, class_weight="balanced", max_depth=None)

# clf = BaggingClassifier(KNeighborsClassifier(), max_samples=0.5, max_features=0.5, n_jobs=8, verbose=True)
# clf = AdaBoostClassifier(n_estimators=100)
# clf = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0,
#                                  max_depth=1)
# print "Training"
clf.fit(all_X_train, y_train.as_matrix().astype(int))
pickle.dump(clf, open("mlp.pkl", "w"))
clf = pickle.load(open("mlp.pkl"))


# feature_names = []
# for name in column_names:
#   for i in range(len(names)):
#     feature_names.append(name + "_" + names[i])
# feature_names.append('has_sequential_nonempty_duplicates')
# feature_names.append('has_internal_or_terminal_empty')
# feature_names.append('has_patty_under_last_cheese')
# feature_names.append('has_internal_bin')
# feature_names.append('empty_prefix_count')
# feature_names.append('empty_topbun_count')
# feature_names.append('topbun_count')
# feature_names.append('bottombun_topbun_count')
# feature_names.append('patty_count')
#dot_data = export_graphviz(clf, out_file="test.dot", feature_names=feature_names)

X_test_categoricals = X_test[column_names]
tX_test_categoricals = enc.fit_transform(X_test_categoricals)
m = csr_matrix([
  X_test['has_sequential_nonempty_duplicates'].astype(int),
  X_test['has_internal_or_terminal_empty'].astype(int),
  X_test['has_patty_under_last_cheese'].astype(int),
  X_test['has_internal_bun'].astype(int),
  X_test['empty_prefix_count'],
  X_test['empty_topbun_prefix'],
  X_test['topbun_count'],
  X_test['bottombun_count'],
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
X_categoricals = X[column_names]
tX_categoricals = enc.fit_transform(X_categoricals)
m = csr_matrix([
  X['has_sequential_nonempty_duplicates'].astype(int),
  X['has_internal_or_terminal_empty'].astype(int),
  X['has_patty_under_last_cheese'].astype(int),
  X['has_internal_bun'].astype(int),
  X['empty_prefix_count'],
  X['empty_topbun_prefix'],
  X['topbun_count'],
  X['bottombun_count'],
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

# df['prediction'] = prediction.astype(bool)


# fp = df[~df.output & df.prediction]
# for index, row in fp.iterrows():
#     print index
#     label_burger([int(layer) for layer in index], True)
