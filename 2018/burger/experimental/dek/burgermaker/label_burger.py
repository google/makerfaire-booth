from constants import MAX_BURGER_HEIGHT
from burger_elements import BurgerElement
def label_burger(burger, debug=False):
  if len(burger) != MAX_BURGER_HEIGHT:
    if debug: print "Burger is wrong size"
    return False
  topbun_pos = None
  for i in range(len(burger)):
    layer = burger[i]
    # base case
    if layer == BurgerElement.empty.value:
      continue
    if layer == BurgerElement.topbun.value:
      topbun_pos = i
      break
    if debug: print "prefix elements must be empty or topbun"
    return False
  if topbun_pos is None:
    if debug: print "Burger does not have topbun"
    return False
  if burger[-1] != BurgerElement.bottombun.value:
    if debug: print "Burger does not have bottombun bottom"
    return False
  for i in range(topbun_pos+1, len(burger)-1):
    if burger[i] == BurgerElement.topbun.value or burger[i] == BurgerElement.bottombun.value:
      if debug: print "Cannot have internal buns"
      return False
  for i in range(topbun_pos+1, len(burger)):
    if burger[i] == BurgerElement.empty.value:
      if debug: print "Cannot have internal or terminal empty"
      return False
  # for i in range(len(burger)-1):
  #   first, second = burger[i], burger[i+1]
  #   if first != BurgerElement.empty.value and second != BurgerElement.empty.value and first == second:
  #     if debug: print "Cannot have identical sequential items"
  #     return False
  for i in range(1, len(burger)-1):
    if burger[i] == BurgerElement.patty.value:
      break
  else:
    if debug: print "Must have at least one patty"
    return False
  last_cheese_index = None
  for i in range(1, len(burger)-1):
    if burger[i] == BurgerElement.cheese.value:
      last_cheese_index = i
  # if last_cheese_index is not None:
  #   for i in range(last_cheese_index+1, len(burger)):
  #     if burger[i] == BurgerElement.patty.value:
  #       break
  #   else:
  #     if debug: print "Must have at patty under last cheese."
  #     return False
  return True
