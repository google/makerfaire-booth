import pandas
import json
import tornado.web

class RankHandler(tornado.web.RequestHandler):
    def initialize(self, connection, burgers, model):
        self.connection = connection
        self.burgers = burgers
        self.model = model

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
                                            
    def get(self):
        result = self.model.rank()
        if result is None:
            self.set_status(404)
            response = {
                "error": "no ranks yet"
                }
        else:
            goodburgers, badburgers, tp, fp, tn, fn, n_votes = result

            response = {
                "goodburgers": list(zip(goodburgers.index, goodburgers.p_burger)),
                "badburgers": list(zip(badburgers.index, badburgers.p_burger)),
                "tp": tp,
                "fp": fp,
                "tn": tn,
                "fn": fn,
                "n_votes": n_votes,
                }
        self.write(json.dumps(response))
