import csv
import pickle
import uuid
import numpy
from burger_checker import check_burger
from exhaustive_burger import ExhaustiveBurger
from random_burger import RandomBurger

if __name__ == '__main__':
  # b = RandomBurger(5000000)
  b = ExhaustiveBurger()
  i = 0
  with open('burgers.csv', 'wb') as csvfile:
    csvfile.write("layer1,layer2,layer3,layer4,layer5,layer6,layer7,layer8,label\n")
    writer = csv.writer(csvfile, delimiter=',')
    try:
      while True:
        burger = b.next_burger()
        is_burger = check_burger(burger, debug=False)
        writer.writerow([layer.value for layer in burger] + [str(is_burger)])
    except StopIteration:
      pass
