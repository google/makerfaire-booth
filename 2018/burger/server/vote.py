import tornado.web

class VoteHandler(tornado.web.RequestHandler):
    def initialize(self, connection):
        self.connection = self.connection
    
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
                                            
    def get(self):
        burger = self.get_argument('burger', '000000')
        vote = bool(self.get_argument('vote', 'true') == 'true')
        cursor = self.connection.cursor
        cursor.execute("INSERT INTO votes VALUES (?, ?)", (burger, vote))
        self.connection.commit()
        cursor.execute("SELECT output FROM labels WHERE burger = ?", (burger,))
        label = bool(cursor.fetchone()[0])
        
        self.write("Burger: %s Vote: %s Label: %s Correct: %s" % (burger, vote, label, vote==label))

