from PIL import Image
from enum import Enum, unique

@unique
class BurgerElement(Enum):
  crown = 0
  lettuce = 1
  tomato = 2
  cheese = 3
  patty = 4
  heel = 5
