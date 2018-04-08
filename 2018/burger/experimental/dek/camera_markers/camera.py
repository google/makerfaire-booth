import numpy as np
import os
import urllib
import tarfile
import sys
sys.path.insert(0, 'utils')
import signal
import functools
from PySide import QtGui, QtCore
import cv2

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.central_widget = QtGui.QWidget(self)
        self.central_layout = QtGui.QHBoxLayout()
        self.central_widget.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)
        self.image_widget = QtGui.QLabel(self)
        self.central_layout.addWidget(self.image_widget)

        self.camera()
        
    def imageTo(self, image, obj):
        pixmap = QtGui.QPixmap.fromImage(image)
        if obj != []:
            p = QtGui.QPainter()
            p.begin(pixmap)
            for item in obj:
                p.setPen(QtCore.Qt.red)
                print item
                x1, y1, x2, y2 = item[1:]
                w = x2-x1
                h = y2-y1
                p.drawRect(x1, y1, w, h)
            p.end ()
            print
                                    
        self.image_widget.setPixmap(pixmap);
    
    def camera(self):
        self.camera = CameraReader()
        self.camera.start()
        self.camera.signal.connect(self.imageTo)

class CameraReader(QtCore.QThread):
    signal = QtCore.Signal(QtGui.QImage, object)
    def __init__(self):
        super(CameraReader, self).__init__()
        self.cam = cv2.VideoCapture(0)
        self.width = long(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = long(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_1000)
        self.parameters =  cv2.aruco.DetectorParameters_create()

    def run(self):

        while True:
            ret, img = self.cam.read()
            expand = np.expand_dims(img, axis=0)
            boxes = []

            corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(img, self.aruco_dict, parameters=self.parameters)
            for i, corner in enumerate(corners):
                ul, ur, lr, ll = corner[0].astype(int)
                pts = np.array([ul, ur, lr, ll])
                pts = [pts.reshape((-1,1,2))]
                print ids[i][0]
                if ids[i][0] == 1:
                    color = (255, 0, 0)
                elif ids[i][0] == 2:
                    color = (0, 255, 0)
                else:
                    color = (0, 0, 255)
                cv2.polylines(img, pts, False, color, thickness=4)
            #for i in range(result['num_detections']):
            #    if result['detection_scores'][i] > 0.5:
            #        class_ = result['detection_classes'][i]
            #        box = result['detection_boxes'][i]
            #        y1, x1 = box[0] * self.width, box[1] * self.height
            #        y2, x2 = box[2] * self.width, box[3] * self.height
            #        boxes.append((class_, x1, y1, x2, y2))
                    
            image = QtGui.QImage(img.data, self.width, self.height, QtGui.QImage.Format_RGB888).rgbSwapped()
            self.signal.emit(image, boxes)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtGui.QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    app.exec_()
