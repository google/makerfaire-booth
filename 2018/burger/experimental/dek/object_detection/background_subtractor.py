import tensorflow as tf
import numpy as np
import os
import urllib
import tarfile
import sys
sys.path.insert(0, 'utils')
import signal
from PySide import QtGui, QtCore
import cv2
from skimage.filters import threshold_local

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
        
    def imageTo(self, image):
        pixmap = QtGui.QPixmap.fromImage(image)
        self.image_widget.setPixmap(pixmap)
    
    def camera(self):
        self.camera = CameraReader()
        self.camera.start()
        self.camera.signal.connect(self.imageTo)

class CameraReader(QtCore.QThread):
    signal = QtCore.Signal(QtGui.QImage)
    def __init__(self):
        super(CameraReader, self).__init__()
        self.cam = cv2.VideoCapture(0)
        self.width = long(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = long(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def run(self):
        while True:
            ret, img = self.cam.read()
            if ret:

                block_size = 35
                bw = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                adaptive_thresh = threshold_local(bw, block_size, offset=10)
                binary_adaptive = bw > adaptive_thresh
                img[binary_adaptive] = (0,0,0)
                image = QtGui.QImage(img.data, self.width, self.height, QtGui.QImage.Format_RGB888)
                self.signal.emit(image)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtGui.QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    app.exec_()
