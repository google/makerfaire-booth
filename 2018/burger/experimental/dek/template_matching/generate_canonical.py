import numpy
import os
import math
import sys
import rsvg
import cairo
sys.path.insert(0, "../../../machine")
from burger_elements import BurgerElement


handles = {}
for layer in BurgerElement.__members__:
  if layer != 'empty':
    layer_name = "../../../assets/%s.svg" % layer
    handles[layer] = rsvg.Handle(layer_name)

layers = BurgerElement.__members__.keys()

  
def draw_example(layer, width, height, scale, clear_background=True):
    img = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(img)
    handle = handles[layer]
    dims = handle.get_dimension_data()[2:]
    if clear_background:
        ctx.set_source_rgb (255,255,255)
        ctx.paint()
    
    ctx.translate(width/2 - dims[0]/2, height/2 - dims[1]/2)
    ctx.translate(dims[0]/2, dims[1]/2)
    ctx.scale(scale, scale)
    ctx.translate(-dims[0]/2, -dims[1]/2)
    handle.render_cairo(ctx)

    return img

def get_bbox(a, width, height):
    alpha = a[:, :, 3]
    x = numpy.where(alpha != 0)
    bbox = numpy.min(x[1]), numpy.min(x[0]), numpy.max(x[1]), numpy.max(x[0])
    return bbox

def main():
    width = 256
    height = 256
    scale = 2
    for layer in layers[1:]:
        img = draw_example(layer, width, height, scale, clear_background=False)
        a = numpy.ndarray(shape=(width, height, 4), dtype=numpy.uint8, buffer=img.get_data())
        a = a[...,[2,1,0,3]]
        bbox = get_bbox(a, width, height)
        crop_width = (bbox[2]-bbox[0])*2
        crop_height = (bbox[3]-bbox[1])*2
        img = draw_example(layer, crop_width, crop_height, scale)
        
        img.write_to_png(os.path.join("canonical", layer + ".png"))


if __name__ == '__main__':
    main()
