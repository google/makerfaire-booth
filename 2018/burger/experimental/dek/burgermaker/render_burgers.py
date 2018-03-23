import numpy
import os
import itertools
import cairo
import rsvg
import pandas
from burger_elements import BurgerElement
from sklearn.model_selection import train_test_split

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


def write_group(group, dir_):
  rows = group[['layer0','layer1','layer2','layer3','layer4','layer5']]
  burgercounter = 0
  notburgercounter = 0
  for index, row in rows.iterrows():
    burger = [BurgerElement(item).name for item in row]
    label = group.loc[index]['output']
    if label == True:
      name = os.path.join(dir_, "burgers", "burger%05d" % burgercounter + ".png")
      burgercounter += 1
    else:
      name = os.path.join(dir_, "notburgers", "notburger%05d" % notburgercounter + ".png")
      notburgercounter += 1
      
    img = render_burger(burger, item)
    img.write_to_png(name)

df = pandas.read_hdf('data.h5', 'df')
pos = df[df.output == True]
neg = df[df.output == False]
# neg_sampled = neg.sample(len(pos)*500)
dataset = pos.append(neg)
X = dataset.drop(['output'], axis=1)
y = dataset['output']
X_train, X_test, y_train, y_test = train_test_split(X, y)
Xy_train = pandas.concat([X_train,y_train], axis=1)
Xy_test = pandas.concat([X_test,y_test], axis=1)

write_group(Xy_train, 'data/train')
write_group(Xy_test, 'data/validation')
# write_group(pos.append(neg), 'data/all')
