import os
import itertools
from enum import Enum, unique
import cairo
import rsvg


MAX_BURGER_HEIGHT=6

@unique
class BurgerElement(Enum):
  empty = 0
  topbun = 1
  lettuce = 2
  tomato = 3
  cheese = 4
  patty = 5
  bottombun = 6

handles = {}
for layer in BurgerElement.__members__:
  if layer != 'empty':
    layer_name = "../../../assets/%s.svg" % layer
    handles[layer] = rsvg.Handle(layer_name)
  
burgers_it = itertools.product(BurgerElement.__members__, repeat=MAX_BURGER_HEIGHT)
burgers = list(burgers_it)
for burger in burgers:
  img = cairo.ImageSurface(cairo.FORMAT_ARGB32, 72, 120)
  ctx = cairo.Context(img)
  ctx.translate(0, -10)
  for i in range(6):
    layer = burger[i]
    if layer != 'empty':
      handles[layer].render_cairo(ctx)
    ctx.translate(0, 20)
  name = os.path.join('render', ",".join(burger) + ".png")
  img.write_to_png(name)
