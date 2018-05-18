import pandas
import json
import tornado.web

class LabelHandler(tornado.web.RequestHandler):
    def initialize(self, burgers, model):
        self.burgers = burgers
        self.model = model

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
                                            
    def get(self):
        burger = self.get_argument('burger')
        result = self.model.label([int(item) for item in list(burger)])
        if result is None:
            self.set_status(404)
            response = {
                "error": "no labels yet"
                }
        else:
            response = {
                "label": result[0],
                }
        self.write(json.dumps(response))
