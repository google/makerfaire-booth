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
  good_burgers = set()
  bad_burgers = set()

  # b = RandomBurger(5000000)
  b = ExhaustiveBurger()
  i = 0
  try:
    while True:
      burger = b.next_burger()
      if burger not in all_burgers:
        all_burgers.add(burger)

        if burger not in good_burgers:
          if check_burger(burger, debug=False):
            good_burgers.add(burger)
            print "Found new good burger", i, burger
            i += 1

            # dwg = svg_burger(burger)
            # name = ''.join([str(layer.value) for layer in burger])
            # dwg.saveas('output/%s.svg' % name)
          else:
            bad_burgers.add(burger)


  except StopIteration:
    all_burgers_labelled = set()
    for burger in good_burgers:
      labelled_burger = [layer.name for layer in burger]
      labelled_burger.append("True")
      all_burgers_labelled.add(tuple(labelled_burger))
    for burger in bad_burgers:
      labelled_burger = [layer.name for layer in burger]
      labelled_burger.append("False")
      all_burgers_labelled.add(tuple(labelled_burger))
      

    o = open("burgers.csv", "w")
    for burger in all_burgers_labelled:
      o.write(','.join(burger))
      o.write("\n")
    o.close()
