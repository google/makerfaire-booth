import pickle
import pandas
import os
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
column_names = ['layer0', 'layer1', 'layer2', 'layer3', 'layer4', 'layer5']
enc = OneHotEncoder(n_values=[7,7,7,7,7,7])
    
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
    burgers = pandas.read_hdf('../machine/data.h5', 'df')
    X = burgers.drop(['output'], axis=1)
    y = burgers['output']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5)
    if os.path.exists('split.h5'):
        os.remove('split.h5')
    X_train.join(y_train).to_hdf('split.h5', 'train', format='fixed')
    X_test.join(y_test).to_hdf('split.h5', 'test', format='fixed')

    clf = MLPClassifier(solver='adam',
                        activation='relu',
                        hidden_layer_sizes=64,
                        verbose=True,
                        max_iter=100,
                        tol=1e-4,
                        random_state=1)
    pickle.dump(clf, open("clf.pkl", "wb"))

if __name__ == '__main__':
    main()
    
