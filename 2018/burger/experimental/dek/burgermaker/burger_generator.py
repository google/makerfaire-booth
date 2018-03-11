import csv
import sys
import pandas
from burger_checker import check_burger
from exhaustive_burger import ExhaustiveBurger
from random_burger import RandomBurger
#from burger_features import featurize_burgers
sys.path.insert(0, "../burgerdata")
from burger_data import BurgerElement
from burger_index import burger_to_index

if __name__ == '__main__':
  # b = RandomBurger(5000000)
  b = ExhaustiveBurger()
  i = 0
  
  burgers = []
  try:
    while True:
      burger = b.next_burger()
      print burger_to_index(burger), str(check_burger(burger)).lower()
      # burgers.append(burger)
  except StopIteration:
    pass
    # index = pandas.Series([burger_to_index(burger) for burger in burgers], dtype=str)
    # index.to_csv("burgers.csv")
  #   df = pandas.DataFrame(burgers,
  #                         index = index,
  #                         columns = ['layer1', 'layer2', 'layer3', 'layer4', 'layer5', 'layer6', 'layer7', 'layer8'])
  #   df.to_pickle("burgers.pkl")

  # burgers = pandas.read_pickle('burgers.pkl')
  # featurize_burgers(burgers)
  # df.to_csv("burger_features.csv")
  
