import glob
import itertools
import os
import io
import sys
import numpy
from PIL import Image
import tensorflow as tf
import random
from object_detection.utils import dataset_util
sys.path.insert(0, "../../../machine")
from burger_elements import BurgerElement


flags = tf.app.flags
flags.DEFINE_string('output_path', 'label.records', 'Path to output TFRecord')
FLAGS = flags.FLAGS
layers = BurgerElement.__members__.keys()

def get_example(fname):

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


def create_tf_example(filename, writer):
    classes_text = []
    classes = []
    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    image_filename = os.path.join("/home/dek/movie", os.path.basename(filename)[:-7])
    im = Image.open(image_filename)
    arr = io.BytesIO()
    im.save(arr, format='PNG')
    height = im.height
    width = im.width
    encoded_image_data = arr.getvalue()
    image_format = 'png'
    for line in open(filename).readlines():
        data = line.split(",")
        bbox = map(int, map(float, data[:4]))
        class_text = data[4].strip()
        class_idx = BurgerElement[class_text].value
        classes_text.append(class_text)
        classes.append(class_idx)
        xmins.append(bbox[0]/float(width))
        xmaxs.append(bbox[2]/float(width)) # List of normalized right x coordinates in bounding box
        ymins.append(bbox[1]/float(height)) # List of normalized top y coordinates in bounding box (1 per box)
        ymaxs.append(bbox[3]/float(height)) # List of normalized bottom y coordinates in bounding box


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
  
    writer = tf.python_io.TFRecordWriter(FLAGS.output_path)
    g = glob.glob("labels/*labels")
    for filename in g:
        tf_example = create_tf_example(filename, writer)


    writer.close()


if __name__ == '__main__':
  tf.app.run()
