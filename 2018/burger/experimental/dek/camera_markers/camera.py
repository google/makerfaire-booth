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
        self.image2_widget = QtGui.QLabel(self)
        self.central_layout.addWidget(self.image2_widget)
        
        self.camera()
        
    def imageTo(self, image, image2):
        pixmap = QtGui.QPixmap.fromImage(image)
        p = pixmap.scaledToWidth(1024)
        self.image_widget.setPixmap(p)
        if image2:
            pixmap2 = QtGui.QPixmap.fromImage(image2)
            self.image2_widget.setPixmap(pixmap2)
    
    def camera(self):
        self.camera = CameraReader()
        self.camera.start()
        self.camera.signal.connect(self.imageTo)

class CameraReader(QtCore.QThread):
    signal = QtCore.Signal(QtGui.QImage, QtGui.QImage)
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
                cv2.aruco.drawDetectedMarkers(img, corners, ids)
                for corner in corners:
                    rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(corner, 0.195, newcameramtx, self.dist)
                    try:
                        cv2.aruco.drawAxis(img, newcameramtx, self.dist, rvec, tvec, 0.1)
                    except cv2.error:
                        print "bad matrix"

                d = {}
                if ids is None:
                    image = QtGui.QImage(img.data, w, h, QtGui.QImage.Format_RGB888).rgbSwapped()
                    image2 = None
                else:
                    short_ids = [id_[0] for id_ in ids]
                    for i, corner in enumerate(corners):
                        d[short_ids[i]] = corner
                    try:
                        ul = d[3][0][2]
                        ur = d[2][0][3]
                        lr = d[0][0][0]
                        ll = d[1][0][1]
                    except:
                        image = QtGui.QImage(img.data, w, h, QtGui.QImage.Format_RGB888).rgbSwapped()
                        image2 = None
                    else:
                        pts = np.array([ul, ur, lr, ll], np.int32)
                        pts = pts.reshape((-1,1,2))
                        cv2.polylines(img,[pts],True,(0,255,255))
                        # rect = cv2.boundingRect(np.array([ul, ur, lr, ll]))
                        # ul = rect[0], rect[1]
                        # ur = rect[0] + rect[2], rect[1]
                        # lr = rect[0] + rect[2], rect[1] + rect[3]
                        # ll = rect[0], rect[1] + rect[3]
                        # pts = np.array([ul, ur, lr, ll], np.int32)
                        # pts = pts.reshape((-1,1,2))
                        # cv2.polylines(img,[pts],True,(255,0,255))

                        # crop = img[rect[1]:rect[1]+rect[3],
                        #            rect[0]:rect[0]+rect[2]]

                        # crop = np.ascontiguousarray(crop)
                        # crop_h, crop_w, _ = crop.shape
                        image = QtGui.QImage(img.data, w, h, QtGui.QImage.Format_RGB888).rgbSwapped()
                        # image2 = QtGui.QImage(crop.data, crop_w, crop_h, 3*crop_w, QtGui.QImage.Format_RGB888).rgbSwapped()

                        destCorners = np.array([ [0, 0], [128, 0], [128, 128], [0, 128]], dtype=np.float32)
                        srcCorners = np.array([ul, ur, lr, ll], dtype=np.float32)
                        pt = cv2.getPerspectiveTransform(srcCorners, destCorners)
                        result = cv2.warpPerspective(img, pt, (128, 128))
                        image2 = QtGui.QImage(result.data, 128, 128, 3*128, QtGui.QImage.Format_RGB888).rgbSwapped()

                self.signal.emit(image, image2)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtGui.QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    app.exec_()
