from constants import MAX_BURGER_HEIGHT
from burger_elements import BurgerElement
import collections

def count(burger):
    return collections.Counter(burger)

def has_sequential_nonempty_duplicates(burger):
  for i in range(len(burger)-1):
    first, second = burger[i], burger[i+1]
    if first != BurgerElement.empty.value and second != BurgerElement.empty.value and first == second:
      return False
  return True

# def get_topbun_pos(burger):
#   topbun_pos = None
#   for i in range(len(burger)):
#     layer = burger[i]
#     # base case
#     if layer == BurgerElement.empty.value:
#       continue
#     if layer == BurgerElement.topbun.value:
#       topbun_pos = i
#       break
#     break
#   return topbun_pos

def has_internal_or_terminal_empty(burger):
  i = 0
  # Consume initial empties
  while i < MAX_BURGER_HEIGHT:
    if burger[i] != BurgerElement.empty.value:
      break
    i += 1
    
  # Consume subsequent non-empties
  while i < MAX_BURGER_HEIGHT:
    if burger[i] == BurgerElement.empty.value:
      return True
    i += 1
    
  return False

def has_internal_bun(burger):
  i = 0
  # Consume initial topbun
  while i < MAX_BURGER_HEIGHT-1:
    if burger[i] == BurgerElement.topbun.value:
      break
    i += 1

  if i == MAX_BURGER_HEIGHT-1:
    return False

  while i < MAX_BURGER_HEIGHT-1:
    if burger[i] == BurgerElement.topbun.value or burger[i] == BurgerElement.bottombun.value:
      return True
    i += 1

  return False


def empty_prefix_count(burger):
  i = 0
  while i < MAX_BURGER_HEIGHT:
    if burger[i] != BurgerElement.empty.value:
      break
    i += 1
  return i

def empty_topbun_prefix(burger):
  i = 0
  while i < MAX_BURGER_HEIGHT:
    if burger[i] == BurgerElement.empty.value:
      i += 1
      continue
    if burger[i] == BurgerElement.topbun.value:
      break
    return False
  return True

def has_patty_under_last_cheese(burger):
  last_cheese = None
  for i in range(len(burger)):
    if burger[i] == BurgerElement.cheese.value:
      last_cheese = i
  if last_cheese is None:
    return True
  for i in range(last_cheese+1, len(burger)):
    if burger[i] == BurgerElement.patty.value:
      return True
  return False

  
def count(burger):
  c = collections.Counter(burger)
  return c

def topbun_count(burger):
  count = 0
  for i in range(len(burger)):
    if burger[i] == BurgerElement.topbun.value:
      count += 1
  return count
def bottombun_count(burger):
  count = 0
  for i in range(len(burger)):
    if burger[i] == BurgerElement.bottombun.value:
      count += 1
  return count
