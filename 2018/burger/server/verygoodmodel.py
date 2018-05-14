import random
import numpy
import pickle
import pandas
import os
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, precision_recall_fscore_support
from sklearn.model_selection import train_test_split
column_names = ['layer0', 'layer1', 'layer2', 'layer3', 'layer4', 'layer5']
from one_hot import get_one_hot
enc = get_one_hot()
    
def print_eval(y, prediction):
    print(accuracy_score(y, prediction))
    cf = confusion_matrix(y, prediction)

    tp, fp, tn, fn = cf[1][1], cf[0][1], cf[0][0], cf[1][0]
    
    print("TP:", tp)
    print("FP:", fp)
    print("TN:", tn)
    print("FN:", fn)
    print("FPR:", fp/float(fp+tn))
    print("FNR:", fn/float(fn+tp))

def main():
    burgers = pandas.read_hdf('../data/data.h5', 'df')
    X = burgers.drop(['output'], axis=1)
    y = burgers['output']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5)
    if os.path.exists('split.h5'):
        os.remove('split.h5')
    X_train.join(y_train).to_hdf('split.h5', 'train', format='fixed')
    X_test.join(y_test).to_hdf('split.h5', 'test', format='fixed')

    clf = MLPClassifier(solver='adam',
                        activation='relu',
                        hidden_layer_sizes=(128,128),
                        verbose=True,
                        max_iter=1000,
                        tol=1e-8,
                        random_state=1)
    all_train = X_train.join(y_train)
    pos_train = all_train[all_train.output == True]
    neg_train = all_train[all_train.output == False]
    train = pos_train.append(neg_train.sample(len(pos_train)*1000))
    train_X = train.drop(['output'], axis=1)
    train_y = train['output']
    train_X_categoricals = train_X[column_names]
    ttrain_X_categoricals = enc.fit_transform(
        train_X_categoricals)
    clf.fit(ttrain_X_categoricals,
            train.output)
    classes = numpy.unique(y_train)
    X_test_categoricals = X_test[column_names]
    tX_test_categoricals = enc.fit_transform(X_test_categoricals)
    prediction = clf.predict(tX_test_categoricals)
    accuracy = accuracy_score(y_test, prediction)
    cf = confusion_matrix(y_test, prediction)
    tp, fp, tn, fn = cf[1][1], cf[0][1], cf[0][0], cf[1][0]
    p, r, f1, s = precision_recall_fscore_support(y_test, prediction)
    print(tp,fp,tn,fn)

if __name__ == '__main__':
    main()
    
