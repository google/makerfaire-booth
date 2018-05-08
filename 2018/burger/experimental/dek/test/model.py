from __future__ import print_function
import os
import pickle
import pandas
import numpy
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
column_names = ['layer0', 'layer1', 'layer2', 'layer3', 'layer4', 'layer5']

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
    enc = OneHotEncoder(n_values=[7,7,7,7,7,7])
    burgers = pandas.read_hdf('../../../machine/data.h5', 'df')
    
    X = burgers.drop(['output'], axis=1)
    y = burgers['output']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5)
    
    clf = MLPClassifier(solver='adam',  activation='relu',
                        hidden_layer_sizes=64,
                        verbose=False,
                        max_iter=10000,
                        tol=1e-9,
                        random_state=1)
    classes = numpy.unique(y)
    i = 0
    while True:
        burgers = X_train[y_train == 1]
        notburgers = X_train[y_train == 0]
        # Pull 32 samples from training data,
        # where half the samples come from each class
        sample = burgers.sample(16).join(y_train)
        sample = sample.append(notburgers.sample(16).join(y_train))
        sample_X_train = sample.drop(['output'], axis=1)
        sample_y_train = sample['output']
        sample_X_train_categoricals = sample_X_train[column_names]
        tX_sample_train_categoricals = enc.fit_transform(sample_X_train_categoricals)
        clf.partial_fit(tX_sample_train_categoricals, sample_y_train.as_matrix().astype(int), classes=classes)

        if (i % 5) == 0:
            print(i)
            X_test_categoricals = X_test[column_names]
            tX_test_categoricals = enc.fit_transform(X_test_categoricals)
            prediction = clf.predict(tX_test_categoricals)
            print_eval(y_test, prediction)
            print(classification_report(y_test, prediction))
        i += 1

        X_train_categoricals = X_train[column_names]
        tX_train_categoricals = enc.fit_transform(X_train_categoricals)
        probs = clf.predict_proba(tX_train_categoricals)
        # Store the probabilities
        X_train_copy = X_train.copy()
        X_train_copy['prob_notburger'] = probs[:,0]
        X_train_copy['prob_burger'] = probs[:,1]

        X_train_categoricals = X_train_copy[column_names]
        tX_train_categoricals = enc.fit_transform(X_train_categoricals)
        prediction = clf.predict(tX_train_categoricals)

        
        pickle.dump(clf, open("clf.pkl.tmp", "wb"))
        os.rename("clf.pkl.tmp", "clf.pkl")
        
        # # # Take worst mispredicted items and retrain
        # mispredicted = X_train_copy[y_train != prediction]
        # worst_burger = mispredicted.nlargest(1, "prob_burger", keep='first').drop(['prob_burger', 'prob_notburger'], axis=1).join(y_train)
        # worst_notburger = mispredicted.nsmallest(1, "prob_burger", keep='last').drop(['prob_burger', 'prob_notburger'], axis=1).join(y_train)

        # sample = sample.append(worst_burger)
        # sample = sample.append(worst_notburger)
if __name__ == '__main__':
    main()
