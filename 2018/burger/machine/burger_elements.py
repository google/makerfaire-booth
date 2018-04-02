from enum import Enum, unique

@unique
class BurgerElement(Enum):
  empty = 0
  topbun = 1
  lettuce = 2
  tomato = 3
  cheese = 4
  patty = 5
  bottombun = 6
