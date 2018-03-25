import numpy
import os
import itertools
import cairo
import rsvg
import pandas
from burger_elements import BurgerElement

handles = {}
for layer in BurgerElement.__members__:
  if layer != 'empty':
    layer_name = "../../../assets/%s.svg" % layer
    handles[layer] = rsvg.Handle(layer_name)

def render_burger(burger):
  img = cairo.ImageSurface(cairo.FORMAT_ARGB32, 299, 299)
  ctx = cairo.Context(img)
  ctx.translate(110, 80)
  for i in range(6):
    layer = burger[i]
    if layer != 'empty':
      handles[layer].render_cairo(ctx)
    ctx.translate(0, 20)
  return img


def write_group(group, dir_, oversample_burgers=1):
  rows = group[['layer0','layer1','layer2','layer3','layer4','layer5']]
  burgercounter = 0
  notburgercounter = 0
  for index, row in rows.iterrows():
    burger = [BurgerElement(item).name for item in row]
    burgername = "".join([str(BurgerElement(item).value) for item in row])
    label = group.loc[index]['output']
    if label == True:
      for i in range(oversample_burgers):
        name = os.path.join(dir_, "burgers", "burger_" + burgername + ".png")
        img = render_burger(burger)
        img.write_to_png(name)
        burgercounter += 1
    else:
      name = os.path.join(dir_, "notburgers", "notburger_" + burgername + ".png")
      img = render_burger(burger)
      img.write_to_png(name)
      notburgercounter += 1

write_group(pos.append(neg), 'data/all', oversample_burgers=1)
