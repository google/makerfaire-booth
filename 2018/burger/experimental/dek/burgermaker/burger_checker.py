import sys
sys.path.insert(0, "../burgerdata")
from burger_data import BurgerElement

def check_burger(burger, debug=False):
  if len(burger) != 8:
    if debug: print "Burger is wrong size"
    return False
  crown_pos = None
  for i in range(len(burger)):
    layer = burger[i]
    # base case
    if layer == BurgerElement.empty:
      continue
    if layer == BurgerElement.crown:
      crown_pos = i
      break
    if debug: print "prefix elements must be empty or crown"
    return False
  if crown_pos is None:
    if debug: print "Burger does not have crown"
    return False
  if burger[-1] != BurgerElement.heel:
    if debug: print "Burger does not have heel bottom"
    return False
  for i in range(crown_pos+1, len(burger)-1):
    if burger[i] == BurgerElement.crown or burger[i] == BurgerElement.heel:
      if debug: print "Cannot have internal buns"
      return False
  for i in range(crown_pos+1, len(burger)):
    if burger[i] == BurgerElement.empty:
      if debug: print "Cannot have internal or terminal empty"
      return False
  for i in range(len(burger)-1):
    first, second = burger[i], burger[i+1]
    if first != BurgerElement.empty and second != BurgerElement.empty and first == second:
      if debug: print "Cannot have identical sequential items"
      return False
  for i in range(1, len(burger)-1):
    if burger[i] == BurgerElement.patty:
      break
  else:
    if debug: print "Must have at least one patty"
    return False
  last_cheese_index = None
  for i in range(1, len(burger)-1):
    if burger[i] == BurgerElement.cheese:
      last_cheese_index = i
  if last_cheese_index is not None:
    for i in range(last_cheese_index+1, len(burger)):
      if burger[i] == BurgerElement.patty:
        break
    else:
      if debug: print "Must have at patty under last cheese."
      return False


  return True

if __name__ == '__main__':
  test_burgers = [
    [BurgerElement.crown, BurgerElement.lettuce, BurgerElement.tomato, BurgerElement.cheese, BurgerElement.patty, BurgerElement.cheese, BurgerElement.patty, BurgerElement.heel],
    [BurgerElement.crown, BurgerElement.empty, BurgerElement.tomato, BurgerElement.cheese, BurgerElement.patty, BurgerElement.cheese, BurgerElement.patty, BurgerElement.heel],
    [BurgerElement.tomato, BurgerElement.crown, BurgerElement.tomato, BurgerElement.cheese, BurgerElement.patty, BurgerElement.cheese, BurgerElement.patty, BurgerElement.heel],
    [BurgerElement.crown, BurgerElement.lettuce, BurgerElement.tomato, BurgerElement.cheese, BurgerElement.patty, BurgerElement.cheese, BurgerElement.patty, BurgerElement.tomato],
    [BurgerElement.crown, BurgerElement.tomato, BurgerElement.tomato, BurgerElement.cheese, BurgerElement.patty, BurgerElement.cheese, BurgerElement.patty, BurgerElement.heel],
    [BurgerElement.crown, BurgerElement.lettuce, BurgerElement.tomato, BurgerElement.lettuce, BurgerElement.tomato, BurgerElement.lettuce, BurgerElement.tomato, BurgerElement.heel],
    [BurgerElement.crown, BurgerElement.lettuce, BurgerElement.tomato, BurgerElement.lettuce, BurgerElement.tomato, BurgerElement.patty, BurgerElement.cheese, BurgerElement.heel],
    [BurgerElement.heel, BurgerElement.patty, BurgerElement.heel, BurgerElement.patty, BurgerElement.heel, BurgerElement.patty, BurgerElement.crown, BurgerElement.heel]
  ]

  for test_burger in test_burgers:
    print test_burger
    print check_burger(test_burger, debug=True)

