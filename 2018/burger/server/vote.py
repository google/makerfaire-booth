import tornado.web
import sqlite3
import pandas
burgers = pandas.read_hdf('../machine/data.h5', 'df')
connection = sqlite3.connect('server.db')

class VoteHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
                                            
    def get(self):
        burger = self.get_argument('burger', '000000')
        vote = bool(self.get_argument('vote', 'true') == 'true')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO votes VALUES (?, ?)", (burger, vote))
        connection.commit()
        user_label = str(vote).lower()
        true_label = str(burgers.loc[burger]['output']).lower()
        correct = str(vote==true_label).lower()
        self.write('{ "burger": "%s", "user label": %s, "true label": %s, "correct": %s }' % (burger, user_label, true_label, correct))


