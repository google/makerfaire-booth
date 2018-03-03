import random
from burger_data import BurgerElement
burger_element_keys = BurgerElement.__members__.keys()


class RandomBurger:
  # Generate a random, possibly valid burger
  def next_burger(self):
    state = BurgerElement.crown
    burger = [ state ]
    while state != BurgerElement.heel:
      c = random.choice(burger_element_keys)
      state = BurgerElement[c]
      burger.append(state)
    return burger
