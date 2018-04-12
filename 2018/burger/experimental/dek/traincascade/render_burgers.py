import os
import math
import numpy
import cairo
import rsvg
import sys
sys.path.insert(0, "../../../machine")
from burger_elements import BurgerElement

width = int(256)
height = int(256)

handles = {}
for layer in BurgerElement.__members__:
  if layer != 'empty':
    layer_name = "../../../assets/%s.svg" % layer
    handle = rsvg.Handle(layer_name)
    # angles = numpy.linspace(0, math.pi*2,10, endpoint=False)
    angles = [0]
    for angle in angles:
      img = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
      ctx = cairo.Context(img)
      ctx.translate(width/2, height/2)
      ctx.rotate(angle)
      ctx.translate(-width/2, -height/2)
      ctx.scale(3,3)
      handle.render_cairo(ctx)
      img.write_to_png(os.path.join("images", layer + ".%.1f.png" % angle))
