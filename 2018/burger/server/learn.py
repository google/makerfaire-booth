from __future__ import print_function
import tempfile
import os
import time
import pickle
import pandas
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from constants import column_names
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
    conn = sqlite3.connect('server.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''CREATE TABLE models (serial INTEGER PRIMARY KEY AUTOINCREMENT, filename STRING)''')
    except sqlite3.OperationalError as e:
        print("failed to create table", e)
        pass

    enc = OneHotEncoder(n_values=[7,7,7,7,7,7])
    prevX = None
    
    while True:
        data = pandas.read_sql_query('SELECT layers.burger, votes.vote, layers.layer0, layers.layer1, layers.layer2, layers.layer3, layers.layer4, layers.layer5 FROM layers, votes WHERE layers.burger = votes.burger', conn, index_col='burger')
        all_ = pandas.read_sql_query('SELECT layers.burger, labels.output, layers.layer0, layers.layer1, layers.layer2, layers.layer3, layers.layer4, layers.layer5 FROM layers, labels WHERE layers.burger = labels.burger', conn, index_col='burger')

        X = data.drop(['vote'], axis=1)
        if len(X) == 0:
            print("Waiting on votes")
            time.sleep(10)
            continue
        if len(X) == prevX:
            time.sleep(1)
            continue
        print("Training on", len(X))

        y = data['vote']
        X_categoricals = X[column_names]
        tX_categoricals = enc.fit_transform(X_categoricals)
        clf = MLPClassifier(solver='adam',  activation='relu',
                            hidden_layer_sizes=(32,32),
                            verbose=False,
                            max_iter=10000,
                            tol=1e-9,
                            random_state=1)
        t0 = time.time()
        clf.fit(tX_categoricals, y.as_matrix().astype(int))
        t1 = time.time()
        print("Fit took", t1-t0)
        prevX = len(X)


        t = tempfile.NamedTemporaryFile(delete=False)
        pickle.dump(clf, t)
        t.close()
        cursor.execute("INSERT INTO models(filename) VALUES (?)", [t.name])
        conn.commit()

        # Fit all the data to the model
        X = all_.drop(['output'], axis=1)
        y = all_['output']
        X_categoricals = X[column_names]
        tX_categoricals = enc.fit_transform(X_categoricals)
        prediction = clf.predict(tX_categoricals)
        # Store the predictions 
        all_['prediction'] = prediction
        print("All:")
        print_eval(y, prediction)
        probs = clf.predict_proba(tX_categoricals)
        # Store the probabilities
        all_['prob_notburger'] = probs[:,0]
        all_['prob_burger'] = probs[:,1]

        mispredicted = all_[all_.output != all_.prediction]
        print(mispredicted.nlargest(10, "prob_burger")[['output', 'prediction', 'prob_burger']])
        print()
        print(mispredicted.nsmallest(10, "prob_burger")[['output', 'prediction', 'prob_burger']])
        print()
        
if __name__ == '__main__':
    main()
