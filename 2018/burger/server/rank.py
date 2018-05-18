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
            burgerrank, tp, fp, tn, fn, yes_votes, no_votes = result

            burgerrank_top10 = burgerrank.head(10)
            response = {
                "burgerrank": list(zip(burgerrank_top10.index, burgerrank_top10.p_burger)),
                "tp": int(tp),
                "fp": int(fp),
                "tn": int(tn),
                "fn": int(fn),
                "yes_votes": int(yes_votes),
                "no_votes": int(no_votes),
                }
        self.write(json.dumps(response))
