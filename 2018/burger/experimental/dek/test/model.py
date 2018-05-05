from __future__ import print_function
import pandas
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
column_names = ['layer0', 'layer1', 'layer2', 'layer3', 'layer4', 'layer5']
import sqlite3

def print_eval(y, prediction):
    print(accuracy_score(y, prediction))
    cf = confusion_matrix(y, prediction)

    tp, fp, tn, fn = cf[1][1], cf[0][1], cf[0][0], cf[1][0]
    
    print("TP:", tp)
    print("FP:", fp)
    print("TN:", tn)
    print("FN:", fn)

def main():
    enc = OneHotEncoder(n_values=[7,7,7,7,7,7])
    conn = sqlite3.connect('server.db')
    cursor = conn.cursor()
    all_ = pandas.read_sql_query('SELECT layers.burger, labels.output, layers.layer0, layers.layer1, layers.layer2, layers.layer3, layers.layer4, layers.layer5 FROM layers,labels WHERE layers.burger = labels.burger', conn, index_col='burger')
    

    sample = all_.sample()
    while True:
        print(sample)

        X = sample.drop(['output'], axis=1)
        y = sample['output']

        X_categoricals = X[column_names]
        tX_categoricals = enc.fit_transform(X_categoricals)
        clf = MLPClassifier(solver='adam',  activation='relu',
                            hidden_layer_sizes=(32,32),
                            verbose=False,
                            max_iter=10000,
                            tol=1e-9,
                            random_state=1)
        clf.fit(tX_categoricals, y.as_matrix().astype(int))

        X = all_.drop(['output'], axis=1)
        y = all_['output']
        X_categoricals = X[column_names]
        tX_categoricals = enc.fit_transform(X_categoricals)
        prediction = clf.predict(tX_categoricals)
        print_eval(y, prediction)
        probs = clf.predict_proba(tX_categoricals)
        # Store the probabilities
        all_copy = all_.copy()
        all_copy['prob_notburger'] = probs[:,0]
        all_copy['prob_burger'] = probs[:,1]

        mispredicted = all_copy[all_copy.output != prediction]
        worst_burger = mispredicted.nlargest(1, "prob_burger", keep='first').drop(['prob_burger', 'prob_notburger'], axis=1)
        worst_notburger = mispredicted.nsmallest(1, "prob_burger", keep='last').drop(['prob_burger', 'prob_notburger'], axis=1)
        
        sample = sample.append(worst_burger)
        sample = sample.append(worst_notburger)
if __name__ == '__main__':
    main()
