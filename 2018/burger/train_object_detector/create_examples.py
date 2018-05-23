from __future__ import print_function
import math
import numpy
import os
import random
import sys
sys.path.insert(0, "../constants")
sys.path.insert(0, "../renderer")
from object_detection.utils import dataset_util
from burger_elements import BurgerElement
from PyQt5 import QtGui, QtWidgets, QtCore, QtSvg
import tensorflow as tf

layers = list(BurgerElement.__members__.keys())

WIDTH=256
HEIGHT=256
NUM_LAYERS=1

flags = tf.app.flags
flags.DEFINE_string('train_output_path', '../data/burgers_train.record', 'Path to output TFRecord')
flags.DEFINE_string('eval_output_path', '../data/burgers_eval.record', 'Path to output TFRecord')
FLAGS = flags.FLAGS


def image_as_png(image):
    ba = QtCore.QByteArray()
    buf = QtCore.QBuffer(ba);
    buf.open(QtCore.QIODevice.WriteOnly);
    image.save(buf, "PNG")
    return ba.data()

def get_random_orientation():
    rot = numpy.random.uniform(-180, 180)
    tx = numpy.random.uniform(-64, 64)
    ty = numpy.random.uniform(-64, 64)
    scale = numpy.random.uniform(0.1, 2)
    return rot, tx, ty, scale

class Widget(QtWidgets.QGraphicsView):
    def __init__(self):
        super(Widget, self).__init__()
        self.setFixedSize(WIDTH, HEIGHT)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        scene = QtWidgets.QGraphicsScene()
        self.setScene(scene)
        self.scene().setSceneRect(0, 0, WIDTH, HEIGHT)

        self.timer = QtCore.QTimer.singleShot(0, self.quit)
    def quit(self):
        QtWidgets.QApplication.instance().quit()

    def addItems(self):
        while len(self.scene().items()) < NUM_LAYERS:
            layer = random.choice(layers[1:])
            path = os.path.join("../static/assets", layer + ".svg")

            rot, tx, ty, scale = get_random_orientation()
            item = QtSvg.QGraphicsSvgItem(path)
            item.layer = layer
            item.setPos(WIDTH/2 + tx, WIDTH/2 + ty)
            item.setScale(scale)
            item.setRotation(rot)
            self.scene().addItem(item)
            if item not in self.scene().items(self.sceneRect(), QtCore.Qt.ContainsItemShape):
                self.scene().removeItem(item)
                continue
            else:
                if item.collidingItems(QtCore.Qt.IntersectsItemBoundingRect):
                    self.scene().removeItem(item)
                    continue
                removed = False
                for item2 in self.scene().items():
                    if item != item2:
                        if item.sceneBoundingRect().intersects(item2.sceneBoundingRect()):
                            self.scene().removeItem(item)
                            removed = True
                            break
                if removed:
                    continue

    
        
    def getImage(self):
        image = QtGui.QImage(QtCore.QSize(WIDTH, HEIGHT), QtGui.QImage.Format_RGB888)
        image.fill(QtCore.Qt.white)
        painter = QtGui.QPainter(image)
        self.scene().render(painter)
        painter.end()
        return image

    def getExample(self):
        image = self.getImage()
        png = image_as_png(image)

        bbox = []
        class_text = []
        class_idx = []
        for item in self.items():
            bbox.append(item.sceneBoundingRect().getCoords())
            class_text.append(item.layer)
            class_idx.append(BurgerElement[item.layer].value)
                             
        example = {
            'width': WIDTH,
            'height': HEIGHT,
            'filename': 'arbitrary',
            'encoded_image_data': png,
            'image_format': 'png',
            'bbox': bbox,
            'class_text': class_text,
            'class_idx': class_idx
        }

        return example

def create_tf_example(example, writer):
  height = example['height']
  width = example['width']
  filename = example['filename']
  encoded_image_data = example['encoded_image_data']
  image_format = example['image_format']

  bboxes = example['bbox']
  xmins = [bbox[0]/float(width) for bbox in bboxes] # List of normalized left x coordinates in bounding box (1 per box)
  xmaxs = [bbox[2]/float(width) for bbox in bboxes] # List of normalized right x coordinates in bounding box
  ymins = [bbox[1]/float(height) for bbox in bboxes] # List of normalized top y coordinates in bounding box (1 per box)
  ymaxs = [bbox[3]/float(height) for bbox in bboxes] # List of normalized bottom y coordinates in bounding box
  classes_text = example['class_text']
  classes = example['class_idx']

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

def main():
    app = QtWidgets.QApplication(sys.argv)

    train_writer = tf.python_io.TFRecordWriter(FLAGS.train_output_path)
    eval_writer = tf.python_io.TFRecordWriter(FLAGS.eval_output_path)


    widget = Widget()
    for i in range(10000):
        print(i)
        widget.addItems()
        image = widget.getImage()
        example = widget.getExample()
        writer = train_writer if random.random() < .7 else eval_writer
        create_tf_example(example, writer)
        widget.scene().clear()
    train_writer.close()
    eval_writer.close()

if __name__ == '__main__':
  main()
