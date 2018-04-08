import pickle
import numpy as np
import os
import sys
sys.path.insert(0, 'utils')
import signal
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
        
    def imageTo(self, image):
        pixmap = QtGui.QPixmap.fromImage(image)
        self.image_widget.setPixmap(pixmap);
    
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
        self.aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_1000)
        self.parameters =  cv2.aruco.DetectorParameters_create()
        rms, self.mtx, self.dist, rvecs, tvecs = pickle.load(open("calib.pkl"))

    def run(self):

        while True:
            ret, img = self.cam.read()
            if ret == True:
                h, w, _ = img.shape
                newcameramtx, roi=cv2.getOptimalNewCameraMatrix(self.mtx, self.dist, (w,h), 1, (w,h))
                dst = cv2.undistort(img, self.mtx, self.dist, None, newcameramtx)
                # # crop the image
                x, y, w, h = roi
                dst = dst[y:y+h, x:x+w]
                img = np.ascontiguousarray(dst, dst.dtype)
                h, w, _ = img.shape

                corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(img, self.aruco_dict, parameters=self.parameters)
                cv2.aruco.drawDetectedMarkers(img,corners, ids)
                for corner in corners:
                    rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(corner, 0.05, newcameramtx, self.dist)
                    try:
                        cv2.aruco.drawAxis(img, newcameramtx, self.dist, rvec, tvec, 0.1)
                    except cv2.error:
                        print "bad matrix"
                image = QtGui.QImage(img.data, w, h, QtGui.QImage.Format_RGB888).rgbSwapped()
                self.signal.emit(image)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtGui.QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    app.exec_()
