import sys
import numpy
from PIL import Image
import tensorflow as tf
import rsvg
import cairo

from object_detection.utils import dataset_util
sys.path.insert(0, "../../../../machine")
from burger_elements import BurgerElement


flags = tf.app.flags
flags.DEFINE_string('output_path', '', 'Path to output TFRecord')
FLAGS = flags.FLAGS


def get_image():
    width = int(256)
    height = int(256)

    handles = {}
    layer = 'patty'
    layer_name = "../../../../assets/%s.svg" % layer
    handle = rsvg.Handle(layer_name)
    dims = handle.get_dimension_data()[2:]

    # angles = numpy.linspace(0, math.pi*2,10, endpoint=False)
    img = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(img)
    ctx.translate(width/2 - dims[0]/2, height/2 - dims[1]/2)

    ctx.translate(dims[0]/2, dims[1]/2)
    ctx.rotate(3.14/2)
    ctx.scale(3,3)
    ctx.translate(-dims[0]/2, -dims[1]/2)

    handle.render_cairo(ctx)
    # img.write_to_png(os.path.join("images", layer + ".png"))
    a = numpy.ndarray(shape=(width, height, 4), dtype=numpy.uint8, buffer=img.get_data())

    a= a[...,[2,1,0,3]]

    alpha = a[:, :, 3]
    x = numpy.where(alpha != 0)
    bbox = numpy.min(x[1]), numpy.min(x[0]), numpy.max(x[1]), numpy.max(x[0])

    fname = 'test.png'
    im = Image.fromarray(a, mode='RGBA')
    im.save(fname)
    return fname, bbox


def create_tf_example(example):
  # TODO(user): Populate the following variables from your example.
  height = example['height']
  width = example['width']
  filename = example['filename'] # Filename of the image. Empty if image is not from file
  encoded_image_data = example['encoded_image_data'] # Encoded image bytes
  image_format = example['image_format']

  bbox = example['bbox']
  xmins = [bbox[0]] # List of normalized left x coordinates in bounding box (1 per box)
  xmaxs = [bbox[2]] # List of normalized right x coordinates in bounding box
             # (1 per box)
  ymins = [bbox[1]] # List of normalized top y coordinates in bounding box (1 per box)
  ymaxs = [bbox[3]] # List of normalized bottom y coordinates in bounding box
             # (1 per box)
  classes_text = [example['class_text']] # List of string class name of bounding box (1 per box)
  classes = [example['class_idx']] # List of integer class id of bounding box (1 per box)

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
  return tf_example

def main(_):
  writer = tf.python_io.TFRecordWriter(FLAGS.output_path)

  fname, bbox = get_image()
  t = open(fname).read()
  im = Image.open(fname)
  examples = [{
      'width': im.width,
      'height': im.height,
      'filename': fname,
      'encoded_image_data': t,
      'image_format': 'png',
      'bbox': bbox,
      'class_text': 'patty',
      'class_idx': 0,
      }]

  for example in examples:
    tf_example = create_tf_example(example)
    writer.write(tf_example.SerializeToString())

  writer.close()


if __name__ == '__main__':
  tf.app.run()
