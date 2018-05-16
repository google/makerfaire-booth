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

        self.model.update([list(burger)], [vote])
        # results = self.model.report()

        response = {
            "burger": burger,
            "vote": vote,
            }
        self.write("OK")
        # response.update(results)

        # predictions = self.model.predict(self.burgers)
        # df = pandas.DataFrame(predictions[:,1], columns=['prob_burger'], index=self.burgers.index.values).join(self.burgers.output)
        # import pdb; pdb.set_trace()
        # response['predictions'] = list(predictions[:,1])
        # self.write(json.dumps(response))
        
        # clf = pickle.load(open("../data/trained.pkl", "rb"))
        # s = [list(item) for item in self.burgers.index.values]
        # ts = enc.fit_transform(s)
        # p = clf.predict_proba(ts)
        # self.burgers['p_burger'] = p[:,1]
        # import pdb; pdb.set_trace()
