from constants import column_names
import pandas
import pickle
import sqlite3
import tornado.web
from sklearn.preprocessing import OneHotEncoder

conn = sqlite3.connect('server.db')
c = conn.cursor()

class BurgerHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
                                            
    def get(self):
        c.execute("SELECT seq FROM SQLITE_SEQUENCE WHERE name='models'")
        seq = c.fetchone()[0]
        c.execute("SELECT filename FROM models WHERE rowid=?", str(seq))
        filename = c.fetchone()[0]
        print(filename)
        clf = pickle.load(open(filename, "rb"))
        
        all_ = pandas.read_sql_query('SELECT layers.burger, labels.output, layers.layer0, layers.layer1, layers.layer2, layers.layer3, layers.layer4, layers.layer5 FROM layers, labels WHERE layers.burger = labels.burger', conn, index_col='burger')

        X = all_.drop(['output'], axis=1)
        y = all_['output']
        X_categoricals = X[column_names]
        enc = OneHotEncoder(n_values=[7,7,7,7,7,7])
        tX_categoricals = enc.fit_transform(X_categoricals)
        prediction = clf.predict(tX_categoricals)
        all_['prediction'] = prediction
        probs = clf.predict_proba(tX_categoricals)
        all_['prob_notburger'] = probs[:,0]
        all_['prob_burger'] = probs[:,1]
        mispredicted = all_[all_.output != all_.prediction]
        largest = mispredicted.nlargest(1, "prob_burger").index.values[0]
        smallest = mispredicted.nsmallest(1, "prob_burger").index.values[0]
        # print(mispredicted.nlargest(1, "prob_burger")[['output', 'prediction', 'prob_burger']])
        # print()
        # print(mispredicted.nsmallest(1, "prob_burger")[['output', 'prediction', 'prob_burger']])
        # print()
        self.write('{ "burger": "%s", "notburger": "%s" }' % (smallest, largest))
