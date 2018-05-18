import pickle
import pandas
import json
import tornado.web

class ExportHandler(tornado.web.RequestHandler):
    def initialize(self, model):
        self.model = model

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
                                            
    def get(self):
        self.model.export()
