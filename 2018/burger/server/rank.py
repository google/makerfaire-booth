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
        df = self.model.rank()
        if df is None:
            self.set_status(404)
            response = {
                "error": "no ranks yet"
                }
        else:
            results = list(zip(df.index, df.p_burger))

            response = {
                "results": results
                }
        self.write(json.dumps(response))
