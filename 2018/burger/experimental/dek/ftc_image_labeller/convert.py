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

flags = tf.app.flags
flags.DEFINE_string('output_path', 'records/label.records', 'Path to output TFRecord')
FLAGS = flags.FLAGS
from labels import labels

def create_tf_example(filename, writer):
    lines = open(filename).readlines()
    image_filename = lines[0].strip()[1:]
    classes_text = []
    classes = []
    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    im = Image.open(image_filename)
    arr = io.BytesIO()
    im.save(arr, format='PNG')
    height = im.height
    width = im.width
    encoded_image_data = arr.getvalue()
    image_format = 'png'
    for line in lines[1:]:
        line = line.strip()
        if line == '':
            continue
        data = line.split(",")
        bbox = list(map(int, map(float, data[:4])))
        class_text = data[4].strip()
        class_idx = labels.index(class_text)
        classes_text.append(class_text)
        classes.append(class_idx)
        xmins.append(bbox[0]/float(width))
        xmaxs.append(bbox[2]/float(width)) # List of normalized right x coordinates in bounding box
        ymins.append(bbox[1]/float(height)) # List of normalized top y coordinates in bounding box (1 per box)
        ymaxs.append(bbox[3]/float(height)) # List of normalized bottom y coordinates in bounding box


    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(bytes(filename, "utf-8")),
        'image/source_id': dataset_util.bytes_feature(bytes(filename, "utf-8")),
        'image/encoded': dataset_util.bytes_feature(encoded_image_data),
        'image/format': dataset_util.bytes_feature(bytes(image_format, "utf-8")),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature([bytes(t, "utf-8") for t in classes_text]),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
    }))
    writer.write(tf_example.SerializeToString())

def main(_):
  
    writer = tf.python_io.TFRecordWriter(FLAGS.output_path)
    g = glob.glob("labels/*labels")
    g.sort()
    for filename in g:
        tf_example = create_tf_example(filename, writer)


    writer.close()


if __name__ == '__main__':
  tf.app.run()
