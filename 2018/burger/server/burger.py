from __future__ import print_function
import sys
sys.path.insert(0, "../constants")
from constants import column_names
from burger_elements import BurgerElement
import tornado.web
import random

class BurgerHandler(tornado.web.RequestHandler):
    def initialize(self, burgers, model):
        self.burgers = burgers
        self.model = model

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
                                            
    def get(self):
        difficulty = int(self.get_argument('difficulty', 0))

        if difficulty == 0:
            if random.random() > 0.5:
                burger = list(self.burgers[self.burgers.output == 1].sample().index.values[0])
            else:
                burger = list(self.burgers[self.burgers.output == 0].sample().index.values[0])

        elif difficulty == 1:
            # Return burger with dupe elements
            items = BurgerElement.lettuce.value, BurgerElement.tomato.value, BurgerElement.cheese.value, BurgerElement.patty.value
            dupe = random.choice(items)
            nodupe = list(set(items) - set([dupe]))
            dupepos = random.choice([1,2,3])
            burger = [1]
            for i in range(1,dupepos):
                burger.append(random.choice(nodupe))
            burger.append(dupe)
            burger.append(dupe)
            for i in range(len(burger),5):
                burger.append(random.choice(nodupe))
            burger.append(6)
        elif difficulty == 2:
            # Return burger with cheese below patty
            items = BurgerElement.lettuce.value, BurgerElement.tomato.value
            pattypos = random.choice([1,2,3])
            burger = [1]
            for i in range(1,pattypos):
                burger.append(random.choice(items))
            burger.append(BurgerElement.patty.value)
            burger.append(BurgerElement.cheese.value)
            for i in range(len(burger),5):
                burger.append(random.choice(items))
            burger.append(6)
        elif difficulty == 3:
            # TODO(dek): return highest ranking nonburger
            burger = [1,2,3,4,5,6]
        else:
            burger = [1,2,3,4,5,6]

        burgeridx = u''.join([str(item) for item in burger])
        label = self.burgers.loc[burgeridx].output
        burgerstr = ','.join([str(item) for item in burger])
        self.write('{ "burger": [%s], "label": %d }' % (burgerstr, label))
