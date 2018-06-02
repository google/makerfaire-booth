import traceback
import pickle
import numpy as np
import os
import sys
import signal
from PyQt5 import QtGui, QtCore, QtWidgets, QtSvg
from object_detector import ObjectDetector
import cv2

filename="/home/dek/VID_20180601_095421738.mp4"

from layers import layers

WIDTH=1080
HEIGHT=1920

def intersection(a,b):
    x = max(a[0], b[0])
    y = max(a[1], b[1])
    w = min(a[0]+a[2], b[0]+b[2]) - x
    h = min(a[1]+a[3], b[1]+b[3]) - y
    if w<0 or h<0: return False
    return True

def boxCenter(box):
    return [box[0] + (box[2]-box[0])/2, box[1] + (box[3]-box[1])/2]

class MainWindow(QtWidgets.QGraphicsView):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.scene = QtWidgets.QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, WIDTH, HEIGHT)

        self.setFixedSize(WIDTH, HEIGHT)
        self.setScene(self.scene)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        # self.cam = cv2.VideoCapture(0)
        # self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        # self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
        self.cam = cv2.VideoCapture(filename)
        self.width = int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.cam_pixmap = None
        self.objdet = ObjectDetector()
        
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.camera)
        self.timer.start(0) 

        self.counter = 0

        
    def imageTo(self, pixmap):
        if self.cam_pixmap is None:
            self.cam_pixmap = self.scene.addPixmap(pixmap)
            self.cam_pixmap.setPos(0, 0)
        else:
            self.cam_pixmap.setPixmap(pixmap)

        
    def camera(self):
        ret, img = self.cam.read()
        if ret == True:
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            # img = cv2.resize(img, None, fx=0.25, fy=0.25)
            h, w, _ = img.shape
            image = QtGui.QImage(img.data, w, h, w*3, QtGui.QImage.Format_RGB888).rgbSwapped()
            expand = np.expand_dims(img, axis=0)
            result = self.objdet.detect(expand)
            boxes = []
            for i in range(result['num_detections']):
                if result['detection_scores'][i] > 0.5:
                    class_ = result['detection_classes'][i]
                    box = result['detection_boxes'][i]
                    score = result['detection_scores'][i]
                    y1, x1 = box[0] * h, box[1] * w
                    y2, x2 = box[2] * h, box[3] * w
                    boxes.append((class_, score, x1, y1, x2, y2))
            pixmap = QtGui.QPixmap.fromImage(image)
            p = QtGui.QPainter()
            p.begin(pixmap)
            font = p.font() 
            font.setPointSize (18)
            p.setFont(font)
            for box in boxes:
                p.setPen(QtCore.Qt.red)
                class_, score, x1, y1, x2, y2 = box
                w1 = x2-x1
                h1 = y2-y1
                p.drawRect(QtCore.QRect(QtCore.QPoint(x1, y1), QtCore.QSize(w1, h1)))
                p.drawText(x1, y1, "%s: %5.2f" % (layers[class_-1], score))
            p.end()
            self.imageTo(pixmap)
            pixmap.save("labelled/%05d.png" % self.counter)
            self.counter += 1
        else:
            sys.exit(0)
        #     self.cam = cv2.VideoCapture(filename)
                

class QApplication(QtWidgets.QApplication):
    def __init__(self, *args, **kwargs):
        super(QApplication, self).__init__(*args, **kwargs)
    def notify(self, obj, event):
        try:
            return QtWidgets.QApplication.notify(self, obj, event)
        except Exception:
            print(traceback.format_exception(*sys.exc_info()))
            return False
        
if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    app.exec_()
