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

def render_burger(burger, name):
  img = cairo.ImageSurface(cairo.FORMAT_ARGB32, 72, 120)
  ctx = cairo.Context(img)
  ctx.translate(0, -10)
  for i in range(6):
    layer = burger[i]
    if layer != 'empty':
      handles[layer].render_cairo(ctx)
    ctx.translate(0, 20)
  return img


df = pandas.read_hdf('data.h5', 'df')
pos = df[df.output == True]
neg = df[df.output == False]
neg_sampled = neg.sample(len(pos))


def write_group(group, dir_):
  rows = group[['layer0','layer1','layer2','layer3','layer4','layer5']]
  for index, row in rows.iterrows():
    burger = [BurgerElement(item).name for item in row]
    name = os.path.join(dir_, ",".join(burger) + ".png")
    img = render_burger(burger, item)
    img.write_to_png(name)

write_group(pos, 'pos')
write_group(neg_sampled, 'neg')
