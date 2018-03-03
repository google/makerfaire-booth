from burger_data import BurgerElement

def check_burger(burger, debug=False):
  if len(burger) < 3:
    if debug: print "Burger is too short"
    return False
  if len(burger) > 8:
    if debug: print "Burger is too short"
    return False
  if burger[0] != BurgerElement.crown:
    if debug: print "Burger does not have crown top"
    return False
  if burger[-1] != BurgerElement.heel:
    if debug: print "Burger does not have heel bottom"
    return False
  for i in range(1, len(burger)-1):
    if burger[i] == BurgerElement.crown or burger[i] == BurgerElement.heel:
      if debug: print "Cannot have internal buns"
      return False
  for i in range(len(burger)-1):
    first, second = burger[i], burger[i+1]
    if first == second:
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
