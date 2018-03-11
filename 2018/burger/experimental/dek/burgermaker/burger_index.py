import sys
sys.path.insert(0, "../burgerdata")
from burger_data import BurgerElement

def burger_to_index(burger):
  return ''.join([str(layer.value) for layer in burger])

def index_to_burger(index):
    return [BurgerElement(int(value)) for value in list(index)]


