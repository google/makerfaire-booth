import traceback
import pickle
import numpy as np
import os
import sys
sys.path.insert(0, 'utils')
import signal
from PyQt5 import QtGui, QtCore, QtWidgets
import cv2
from object_detector import ObjectDetector

filename="z:/cut.mkv"

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
    signal2 = QtCore.pyqtSignal(QtGui.QImage, object)
    def __init__(self):
        super(CameraReader, self).__init__()
        self.cam = cv2.VideoCapture(filename)
        #self.cam = cv2.VideoCapture(0)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.width = int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_1000)
        self.parameters =  cv2.aruco.DetectorParameters_create()
        rms, self.mtx, self.dist, rvecs, tvecs = pickle.load(open("calib.pkl","rb"))
        self.objdet = ObjectDetector()

    def run(self):
        counter = 0
        while True:
            ret, img = self.cam.read()
            print(ret)
            if ret == True:
                h, w, _ = img.shape
                newcameramtx, roi=cv2.getOptimalNewCameraMatrix(self.mtx, self.dist, (w,h), 1, (w,h))
                dst = cv2.undistort(img, self.mtx, self.dist, None, newcameramtx)
                # # crop the image
                x, y, w2, h2 = roi
                dst = dst[y:y+h2, x:x+w2]
                img = np.ascontiguousarray(dst, dst.dtype)
                h3, w3, _ = img.shape

                img2 = img.copy()
                corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(img2, self.aruco_dict, parameters=self.parameters)
                cv2.aruco.drawDetectedMarkers(img2, corners, ids)
                for corner in corners:
                    rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(corner, 0.195, newcameramtx, self.dist)
                    try:
                        cv2.aruco.drawAxis(img2, newcameramtx, self.dist, rvec, tvec, 0.1)
                    except cv2.error:
                        print( "bad matrix")
                d = {}
                boxes = []
                image2 = QtGui.QImage(self.width, self.height, QtGui.QImage.Format_RGB888)
                boxes = []
                if ids is None:
                    image = QtGui.QImage(img2.data, w3, h3, w3*3, QtGui.QImage.Format_RGB888).rgbSwapped()
                    self.signal.emit(image)
                else:
                    short_ids = [id_[0] for id_ in ids]
                    for i, corner in enumerate(corners):
                        d[short_ids[i]] = corner
                    if len(d.keys()) != 4:
                        image = QtGui.QImage(img2.data, w3, h3, w3*3, QtGui.QImage.Format_RGB888).rgbSwapped()
                        self.signal.emit(image)
                        continue
                    ul = d[0][0][0]
                    ur = d[1][0][0]
                    lr = d[2][0][0]
                    ll = d[3][0][0]
                    pts = np.array([ul, ur, lr, ll], np.int32)
                    pts = pts.reshape((-1,1,2))
                    cv2.polylines(img,[pts],True,(255,0,255))
                    image = QtGui.QImage(img2.data, w3, h3, w3*3, QtGui.QImage.Format_RGB888).rgbSwapped()
                    self.signal.emit(image)

                    warped_height = 480
                    orig_width = ur[0] - ul[0]
                    orig_height = ll[1] - ul[1]
                    # ratio = orig_width / float(orig_height)
                    ratio = 0.4
                    warped_width = int(round(warped_height * ratio))
                    destCorners = np.array([ [0, 0], [warped_width, 0], [warped_width, warped_height], [0, warped_height]], dtype=np.float32)
                    srcCorners = np.array([ul, ur, lr, ll], dtype=np.float32)
                    pt = cv2.getPerspectiveTransform(srcCorners, destCorners)
                    warped = cv2.warpPerspective(img, pt, (warped_width, warped_height))
                    cv2.imwrite("rectified/%05d.png" % counter, warped)
                    expand = np.expand_dims(warped, axis=0)
                    result = self.objdet.detect(expand)
                    for i in range(result['num_detections']):
                        if result['detection_scores'][i] > 0.5:
                            class_ = result['detection_classes'][i]
                            box = result['detection_boxes'][i]
                            score = result['detection_scores'][i]
                            y1, x1 = box[0] * warped_height, box[1] * warped_width
                            y2, x2 = box[2] * warped_height, box[3] * warped_width
                            boxes.append((class_, score, x1, y1, x2, y2))
                    warped_image = QtGui.QImage(warped.data, warped_width, warped_height, 3*warped_width, QtGui.QImage.Format_RGB888).rgbSwapped()
                    self.signal2.emit(warped_image, boxes)
                    counter += 1
            else:
               sys.exit(0)
#                self.cam = cv2.VideoCapture(filename)
                

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
