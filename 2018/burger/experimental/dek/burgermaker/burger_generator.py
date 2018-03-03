import itertools
import uuid
import numpy
import burger_data
from svg_burger import svg_burger
from burger_checker import check_burger
from exhaustive_burger import ExhaustiveBurger
from random_burger import RandomBurger
from markov_burger import MarkovBurger
from burger_data import BurgerElement

if __name__ == '__main__':
  all_burgers = set()
  good_burgers = set()

  mb = MarkovBurger()
  rb = RandomBurger()
  eb = ExhaustiveBurger()
  i = 0
  while True:
    # burger = tuple(rb.next_burger())
    # burger = tuple(mb.next_burger())
    burger = eb.next_burger()
    if burger not in all_burgers:
      all_burgers.add(burger)

      if burger not in good_burgers:
        if check_burger(burger):
          good_burgers.add(burger)
          print "Found new good burger", i, burger
          i += 1

          dwg = svg_burger(burger)
          name = ','.join([layer.name for layer in burger])
          dwg.saveas('output/%s.svg' % name)
