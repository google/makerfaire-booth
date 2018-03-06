from enum import Enum, unique

@unique
class BurgerElement(Enum):
  empty = 0
  crown = 1
  lettuce = 2
  tomato = 3
  cheese = 4
  patty = 5
  heel = 6
