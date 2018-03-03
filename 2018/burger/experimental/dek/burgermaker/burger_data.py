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

burger_asset = {
    BurgerElement.crown: Image.open('assets/crown.png'),
    BurgerElement.lettuce: Image.open('assets/lettuce.png'),
    BurgerElement.tomato: Image.open('assets/tomato.png'),
    BurgerElement.cheese: Image.open('assets/cheese.png'),
    BurgerElement.patty: Image.open('assets/patty.png'),
    BurgerElement.heel: Image.open('assets/heel.png'),
}
