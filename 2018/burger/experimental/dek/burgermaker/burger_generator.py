import pickle
import itertools
import uuid
import numpy
from svg_burger import svg_burger
from burger_checker import check_burger
from exhaustive_burger import ExhaustiveBurger
from random_burger import RandomBurger

if __name__ == '__main__':
  all_burgers = set()
  all_burgers_labelled = dict()
  good_burgers = set()
  bad_burgers = set()

  # b = RandomBurger(5000000)
  b = ExhaustiveBurger()
  i = 0
  try:
    while True:
      burger = b.next_burger()
      all_burgers_labelled[burger] = check_burger(burger, debug=False)

  except StopIteration:
    o = open("burgers.pkl", "w")
    pickle.dump(all_burgers_labelled, o)
    o.close()
