import itertools
import os
import math
import io
import sys
import numpy
from PIL import Image
import tensorflow as tf
import rsvg
import cairo
import random
from object_detection.utils import dataset_util
sys.path.insert(0, "../../../machine")
from burger_elements import BurgerElement


flags = tf.app.flags
flags.DEFINE_string('train_output_path', '', 'Path to output TFRecord')
flags.DEFINE_string('eval_output_path', '', 'Path to output TFRecord')
FLAGS = flags.FLAGS

handles = {}
for layer in BurgerElement.__members__:
  if layer != 'empty':
    layer_name = "../../../assets/%s.svg" % layer
    handles[layer] = rsvg.Handle(layer_name)

layers = BurgerElement.__members__.keys()

def get_orientations():
  rot = numpy.linspace(-math.pi, math.pi, 10, endpoint=False)
  tx = numpy.linspace(0, 0, 1)
  ty = numpy.linspace(0, 0, 1)
  scale = numpy.linspace(1, 1, 1)
  return rot, tx, ty, scale
  
def get_random_orientation():
    rot = numpy.random.uniform(-math.pi, math.pi)
    tx = numpy.random.uniform(-100, 100)
    ty = numpy.random.uniform(-100, 100)
    scale = numpy.random.uniform(0.25, 4)
    return rot, tx, ty, scale
   
def draw_example(layer, width, height, rot, tx, ty, scale, clear_background=True):
    img = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(img)
    handle = handles[layer]
    dims = handle.get_dimension_data()[2:]
    if clear_background:
        ctx.set_source_rgb (255,255,255)
        ctx.paint()
    
    ctx.translate(width/2 - dims[0]/2, height/2 - dims[1]/2)
    ctx.translate(dims[0]/2, dims[1]/2)
    
    ctx.translate(tx, ty)
    ctx.rotate(rot)
    ctx.scale(scale, scale)
    ctx.translate(-dims[0]/2, -dims[1]/2)
    handle.render_cairo(ctx)

    return img

def get_bbox(a, width, height):
    alpha = a[:, :, 3]
    x = numpy.where(alpha != 0)
    bbox = numpy.min(x[1]), numpy.min(x[0]), numpy.max(x[1]), numpy.max(x[0])
    return bbox

def get_example(layer, rot, tx, ty, scale):
      
    width = int(256)
    height = int(256)

    # angles = numpy.linspace(0, math.pi*2,10, endpoint=False)
    img = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(img)

    img = draw_example(layer, width, height, rot, tx, ty, scale, clear_background=False)
    a = numpy.ndarray(shape=(width, height, 4), dtype=numpy.uint8, buffer=img.get_data())
    a = a[...,[2,1,0,3]]
    bbox = get_bbox(a, width, height)
    x=numpy.array(bbox)
    if numpy.any(x==0):
      return None
    if numpy.any(x==255):
      return None
    
    img = draw_example(layer, width, height, rot, tx, ty, scale, clear_background=True)
    a = numpy.ndarray(shape=(width, height, 4), dtype=numpy.uint8, buffer=img.get_data())
    a = a[...,[2,1,0,3]]
    im = Image.fromarray(a, mode='RGBA')
    arr = io.BytesIO()
    im.save(arr, format='PNG')

    fname = os.path.join("images", "%s_%.2f_%.2f_%.2f_%.2f.png" % (layer, rot, tx, ty, scale))
    if os.path.exists(fname):
      print "already exists", fname
      return None
    else:
      im.save(fname)

    example = {
      'width': im.width,
      'height': im.height,
      'filename': 'arbitrary',
      'encoded_image_data': arr.getvalue(),
      'image_format': 'png',
      'bbox': bbox,
      'class_text': layer,
      'class_idx': BurgerElement[layer].value,
      }

    return example


def create_tf_example(example, writer):
  height = example['height']
  width = example['width']
  filename = example['filename']
  encoded_image_data = example['encoded_image_data']
  image_format = example['image_format']

  bbox = example['bbox']
  # TODO(dek): ensure the bbox indices and width/height are correct
  xmins = [bbox[0]/float(width)] # List of normalized left x coordinates in bounding box (1 per box)
  xmaxs = [bbox[2]/float(width)] # List of normalized right x coordinates in bounding box
  ymins = [bbox[1]/float(height)] # List of normalized top y coordinates in bounding box (1 per box)
  ymaxs = [bbox[3]/float(height)] # List of normalized bottom y coordinates in bounding box
  classes_text = [example['class_text']]
  classes = [example['class_idx']]

  tf_example = tf.train.Example(features=tf.train.Features(feature={
      'image/height': dataset_util.int64_feature(height),
      'image/width': dataset_util.int64_feature(width),
      'image/filename': dataset_util.bytes_feature(filename),
      'image/source_id': dataset_util.bytes_feature(filename),
      'image/encoded': dataset_util.bytes_feature(encoded_image_data),
      'image/format': dataset_util.bytes_feature(image_format),
      'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
      'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
      'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
      'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
      'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
      'image/object/class/label': dataset_util.int64_list_feature(classes),
  }))
  writer.write(tf_example.SerializeToString())

def main(_):
  train_writer = tf.python_io.TFRecordWriter(FLAGS.train_output_path)
  eval_writer = tf.python_io.TFRecordWriter(FLAGS.eval_output_path)


  rots, txs, tys, scales = get_orientations()
  print txs
  all = list(itertools.product(layers[1:], rots, txs, tys, scales))
  print all
  for i, ev in enumerate(all):
    if (i % 1000) == 0:
      print i, i/float(len(all))*100.
    layer, rot, tx, ty, scale = ev
    
    example = get_example(layer, rot, tx, ty, scale)
    if example is None:
        continue
    writer = train_writer if random.random() < .7 else eval_writer
    tf_example = create_tf_example(example, writer)
    
  # while True:
  #   layer = random.choice(layers)
  #   while layer == 'empty':
  #     layer = random.choice(layers)

  #   rot, tx, ty, scale = get_random_orientation()
  #   example = get_example(layer, rot, tx, ty, scale)
  #   if example is None:
  #     continue
  #   writer = train_writer if random.random() < .7 else eval_writer
  #   tf_example = create_tf_example(example, writer)


  # train_writer.close()
  # eval_writer.close()


if __name__ == '__main__':
  tf.app.run()
