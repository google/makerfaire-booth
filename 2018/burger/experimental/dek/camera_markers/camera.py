import pickle
import numpy as np
import os
import sys
sys.path.insert(0, 'utils')
import signal
from PyQt5 import QtGui, QtCore, QtWidgets
import cv2
from object_detector import ObjectDetector

labels = {
    0: 'empty',
    1: 'topbun',
    2: 'lettuce',
    3: 'tomato',
    4: 'cheese',
    5: 'patty',
    6: 'bottombun'
    }

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.central_widget = QtWidgets.QWidget(self)
        self.central_layout = QtWidgets.QHBoxLayout()
        self.central_widget.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)
        self.image_widget = QtWidgets.QLabel(self)
        self.central_layout.addWidget(self.image_widget)
        self.image2_widget = QtWidgets.QLabel(self)
        self.central_layout.addWidget(self.image2_widget)
        
        self.camera()
        
    def imageTo(self, image):
        pixmap = QtGui.QPixmap.fromImage(image)
        self.image_widget.setPixmap(pixmap)

    def imageTo2(self, image2, boxes):
        pixmap2 = QtGui.QPixmap.fromImage(image2)
        p = QtGui.QPainter()
        p.begin(pixmap2)
        for box in boxes:
            p.setPen(QtCore.Qt.red)
            class_, score, x1, y1, x2, y2 = box
            w = x2-x1
            h = y2-y1
            p.drawRect(x1, y1, w, h)
            p.drawText(x1, y1, "%s: %5.2f" % (labels[class_], score))
        p.end ()
        self.image2_widget.setPixmap(pixmap2)

    def camera(self):
        self.camera = CameraReader()
        self.camera.start()
        self.camera.signal.connect(self.imageTo)
        self.camera.signal2.connect(self.imageTo2)

class CameraReader(QtCore.QThread):
    signal = QtCore.pyqtSignal(QtGui.QImage)
    signal2 = QtCore.pyqtSignal(QtGui.QImage,object)
    def __init__(self):
        super(CameraReader, self).__init__()
        self.cam = cv2.VideoCapture(0)
        # self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        # self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.width = int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_1000)
        self.parameters =  cv2.aruco.DetectorParameters_create()
        rms, self.mtx, self.dist, rvecs, tvecs = pickle.load(open("calib.pkl","rb"))
        self.objdet = ObjectDetector()

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
                        print( "bad matrix")
                d = {}
                boxes = []
                image2 = QtGui.QImage(self.width, self.height, QtGui.QImage.Format_RGB888)
                boxes = []
                if ids is None:
                    image = QtGui.QImage(img.data, w, h, w*3, QtGui.QImage.Format_RGB888).rgbSwapped()
                    print("emit image")
                    self.signal.emit(image)
                else:
                    short_ids = [id_[0] for id_ in ids]
                    for i, corner in enumerate(corners):
                        d[short_ids[i]] = corner
                    try:
                        ul = d[0][0][0]
                        ur = d[1][0][0]
                        lr = d[2][0][0]
                        ll = d[3][0][0]
                    except:
                        image = QtGui.QImage(img.data, w, h, w*3, QtGui.QImage.Format_RGB888).rgbSwapped()
                        self.signal.emit(image)
                    else:
                        pts = np.array([ul, ur, lr, ll], np.int32)
                        pts = pts.reshape((-1,1,2))
                        cv2.polylines(img,[pts],True,(0,255,255))
                        image = QtGui.QImage(img.data, w, h, w*3, QtGui.QImage.Format_RGB888).rgbSwapped()

                        warped_height = 640
                        orig_width = ur[0] - ul[0]
                        orig_height = ll[1] - ul[1]
                        ratio = orig_width / float(orig_height)
                        warped_width = int(round(warped_height * ratio))
                        destCorners = np.array([ [0, 0], [warped_width, 0], [warped_width, warped_height], [0, warped_height]], dtype=np.float32)
                        srcCorners = np.array([ul, ur, lr, ll], dtype=np.float32)
                        pt = cv2.getPerspectiveTransform(srcCorners, destCorners)
                        warped = cv2.warpPerspective(img, pt, (warped_width, warped_height))
                        warped_image = QtGui.QImage(warped.data, warped_width, warped_height, 3*warped_width, QtGui.QImage.Format_RGB888).rgbSwapped()
                        image2 = QtGui.QImage(warped_width*2, warped_height*2, QtGui.QImage.Format_RGB888)

                        image2.fill(QtCore.Qt.white);
                        painter = QtGui.QPainter(image2)
                        point = QtCore.QPoint(warped_width/2, warped_height/2)
                        painter.drawImage(point, warped_image)
                        painter.end()
                        bits = image2.constBits().asstring(warped_height*2 * warped_width*2 * 3)
                        img = np.fromstring(bits, dtype=np.uint8).reshape(warped_height*2, warped_width*2, 3)
                        expand = np.expand_dims(img, axis=0)
                        result = self.objdet.detect(expand)
                        for i in range(result['num_detections']):
                            if result['detection_scores'][i] > 0.4:
                                class_ = result['detection_classes'][i]
                                box = result['detection_boxes'][i]
                                score = result['detection_scores'][i]
                                y1, x1 = box[0] * warped_height*2, box[1] * warped_width*2
                                y2, x2 = box[2] * warped_height*2, box[3] * warped_width*2
                                boxes.append((class_, score, x1, y1, x2, y2))
                        self.signal2.emit(image2, boxes)



if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtWidgets.QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    app.exec_()
