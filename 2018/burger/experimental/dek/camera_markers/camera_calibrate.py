import pickle
import numpy as np
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
        self.camera = CameraReader()
        self.camera.signal.connect(self.imageTo)
        self.camera.start()
        self.button = QtGui.QPushButton(self, "Hello")
        self.button.clicked.connect(self.camera.calibrate)
        
    def imageTo(self, image):
        pixmap = QtGui.QPixmap.fromImage(image)
        self.image_widget.setPixmap(pixmap);
    
class CameraReader(QtCore.QThread):
    signal = QtCore.Signal(QtGui.QImage)
    def __init__(self):
        super(CameraReader, self).__init__()
        self.cam = cv2.VideoCapture(0)
        self.width = long(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = long(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_1000)
        self.parameters =  cv2.aruco.DetectorParameters_create()

        self.objpoints = [] # 3d point in real world space
        self.imgpoints = [] # 2d points in image plane
        
    def calibrate(self):
        rms, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(self.objpoints, self.imgpoints, (self.width, self.height), None,None)
        pickle.dump([rms, mtx, dist, rvecs, tvecs], open("calib.pkl", "w"))
            
        
    def run(self):
        # termination criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        objp = np.zeros((6*8,3), np.float32)
        objp[:,:2] = np.mgrid[0:8,0:6].T.reshape(-1,2)


        while True:
            ret, img = self.cam.read()
            # Find the chess board corners
            if ret == True:
                ret, corners = cv2.findChessboardCorners(img, (8,6),None)
                if ret == True:
                    self.objpoints.append(objp)
                    self.imgpoints.append(corners)
                    img = cv2.drawChessboardCorners(img, (8,6), corners, ret)
                image = QtGui.QImage(img.data, self.width, self.height, QtGui.QImage.Format_RGB888).rgbSwapped()
                self.signal.emit(image)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtGui.QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    app.exec_()
