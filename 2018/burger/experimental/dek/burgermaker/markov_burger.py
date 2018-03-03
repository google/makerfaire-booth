import numpy as np
from burger_data import BurgerElement
from burger_checker import check_burger

burger_matrix = np.array([
                                             # FROM:
  [  0,    0.25, 0.25, 0.25, 0.25, 0,     ], #  crown
  [  0,    0,    0.25, 0.25, 0.25, 0.25   ], #  lettuce
  [  0,    0.25, 0,    0.25, 0.25, 0.25   ], #  tomato
  [  0,    0.25, 0.25, 0,    0.25, 0.25   ], #  cheese
  [  0,    0.25, 0.25, 0.25, 0,    0.25   ], #  patty
  [  0,    0,    0,    0,    0,    0,     ], #  heel
  ])
  # TO:
  #  c     l     t     c     p     h
  #  r     e     o     h     a     e
  #  o     t     m     e     t     e
  #  w     t     a     e     t     l
  #  n     u     t     s     t
  #        c     o     e     y
  #        c
  #        e

class MarkovBurger():
  def next_burger(self):
    state = BurgerElement.crown
    burger = [state]
    while state != BurgerElement.heel:
      row = burger_matrix[state.value]
      state = BurgerElement(np.random.choice( len(row), p=row))
      burger.append(state)
    return burger
