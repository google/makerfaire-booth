import json
import tornado.web

class ResetHandler(tornado.web.RequestHandler):
    def initialize(self, connection, model):
        self.connection = connection
        self.model = model

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
                                            
    def get(self):
        self.connection.cursor().execute("DELETE FROM votes")
        self.connection.commit()
