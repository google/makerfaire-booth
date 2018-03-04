import sys
sys.path.insert(0, "../burgerdata")
from burger_data import BurgerElement

def check_burger(burger, debug=False):
  if len(burger) != 8:
    if debug: print "Burger is wrong size"
    return False
  is_empty = None
  crown_pos = None
  for i in range(len(burger)):
    layer = burger[i]
    # base case
    if is_empty is None:
      is_empty = layer == BurgerElement.empty
      continue
    # previous layer was empty
    if is_empty is True:
      if layer == BurgerElement.empty:
        continue
      if layer != BurgerElement.crown:
        if debug: print "Burger does not have crown top"
        return False
      crown_pos = i
      is_empty = False
      continue
    # previous layer was not empty
    if is_empty is False and layer == BurgerElement.empty:
      if debug: print "Burger cannot have internal empty layer"
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

