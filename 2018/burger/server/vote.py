import pandas
import json
import tornado.web

class VoteHandler(tornado.web.RequestHandler):
    def initialize(self, connection, burgers, model):
        self.connection = connection
        self.burgers = burgers
        self.model = model

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
                                            
    def get(self):
        burger = self.get_argument('burger')
        vote_arg = self.get_argument('vote')
        vote = vote_arg == 'true' or vote_arg == 'True'

        self.connection.cursor().execute("INSERT INTO votes (burger, vote) VALUES (?, ?)", (burger, vote))
        self.connection.commit()

        response = {
            "burger": burger,
            "vote": vote,
            "label": bool(self.burgers.loc[burger].output)
            }
        self.write(json.dumps(response))
