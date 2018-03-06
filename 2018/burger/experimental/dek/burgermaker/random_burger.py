import numpy as np
import random
import sys
sys.path.insert(0, "../burgerdata")
from burger_data import BurgerElement
burger_element_keys = BurgerElement.__members__.keys()


class RandomBurger:
  def __init__(self, max_iterations):
    self.max_iterations = max_iterations
    self.iterations = 0

  # Generate a random, possibly valid burger
  def next_burger(self):
    if self.iterations > self.max_iterations:
      raise StopIteration
    state = BurgerElement[np.random.choice(BurgerElement.__members__.keys())]
    burger = [ state ]
    while len(burger) < 8:
      c = random.choice(burger_element_keys)
      state = BurgerElement[c]
      burger.append(state)
    self.iterations += 1
    return tuple(burger)
