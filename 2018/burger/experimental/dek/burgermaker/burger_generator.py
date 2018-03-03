import uuid
import numpy
import random
import burger_data
from burger_data import BurgerElement, burger_asset
from render_burger import render_burger
from burger_checker import check_burger

lengths = numpy.random.normal(6, 3, 1000000).astype(numpy.int)

burger_element_keys = BurgerElement.__members__.keys()

# Generate a random, possibly valid burger
def generate_random_burger(length):
  burger = []
  for i in range(length):
    c = random.choice(burger_element_keys)
    burger.append(BurgerElement[c])
  return burger

if __name__ == '__main__':
  for length in lengths:
    burger = generate_random_burger(length)
    if check_burger(burger):
      print burger
      # icon = render_burger(burger)
      # icon.save('output/%s.png' % uuid.uuid4().hex
