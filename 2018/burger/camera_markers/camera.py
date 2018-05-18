import traceback
import pickle
import numpy as np
import os
import sys
sys.path.insert(0, '../renderer')
import signal
from PyQt5 import QtGui, QtCore, QtWidgets, QtSvg
import cv2
from object_detector import ObjectDetector
from burger_renderer import BurgerRenderer
from classify_burger import BurgerClassifier
# from label_burger import label_burger
sys.path.insert(0, "../constants")
from burger_elements import BurgerElement

filename="z:/cut.mkv"

labels = dict([(member.value, member.name) for member in BurgerElement.__members__.values()])

WIDTH=3840
HEIGHT=2160

CAMERA_WIDTH=1280
CAMERA_HEIGHT=720

WARPED_HEIGHT=720
ratio = 0.4
WARPED_WIDTH = int(round(WARPED_HEIGHT * ratio))

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
        self.scene.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(131, 213, 247)))
        self.scene.setSceneRect(0, 0, WIDTH, HEIGHT)

        self.machine = QtSvg.QGraphicsSvgItem('../static/assets/burger_chute.svg')
        self.scene.addItem(self.machine)
        self.machine.setScale(2)
        self.machine.setPos(1000,0)
 
        self.setFixedSize(WIDTH,HEIGHT)
        self.setScene(self.scene)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.cam = cv2.VideoCapture(0)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
        # # self.cam = cv2.VideoCapture(filename)
        self.width = int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.cam_pixmap = None
        self.aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_1000)
        self.parameters =  cv2.aruco.DetectorParameters_create()
        rms, self.mtx, self.dist, rvecs, tvecs = pickle.load(open("calib.pkl","rb"))
        self.objdet = ObjectDetector()
        self.burger_pixmap = None
        self.rectified_pixmap = None
        font = QtGui.QFont('Arial', 75)
        self.label_text = self.scene.addText("", font)
        self.label_text.setDefaultTextColor(QtCore.Qt.red)
        
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.camera)
        self.timer.start(0) 

        self.counter = 0
        self.burger_classifier = BurgerClassifier()

        font = QtGui.QFont('Arial', 100)
        self.explanation_text = self.scene.addText("test", font)
        self.explanation_text.setHtml("Design your own burger!")
        self.explanation_text.setPos(0, 100)

        font = QtGui.QFont('Arial', 60)
        self.detail_text = self.scene.addText("test", font)
        self.detail_text.setHtml("Place burger layers on the white board<br>Then show the board to the camera<br>Can the computer recognize burgers?<br>Can you fool the computer with a bad burger?")
        self.detail_text.setPos(0, 250)
        
    def imageTo(self, image):
        pixmap = QtGui.QPixmap.fromImage(image)
        pixmap = pixmap.transformed(QtGui.QTransform().scale(-1, 1))

        if self.cam_pixmap is None:
            self.cam_pixmap = self.scene.addPixmap(pixmap)
            self.cam_pixmap.setPos(QtCore.QPointF(50, 2160-720-50))
        else:
            self.cam_pixmap.setPixmap(pixmap)

    def imageTo2Clear(self):
        if self.rectified_pixmap is not None:
            self.scene.removeItem(self.rectified_pixmap)
            self.rectified_pixmap = None
            self.label_text.setPlainText("")
        if self.burger_pixmap is not None:
            self.scene.removeItem(self.burger_pixmap)
            self.burger_pixmap = None
            self.label_text.setPlainText("")
            
    def imageTo2(self, image2, boxes):
        pixmap2 = QtGui.QPixmap.fromImage(image2)
        boxes = self.analyzeBoxes(boxes)
        p = QtGui.QPainter()
        p.begin(pixmap2)
        for box in boxes:
            p.setPen(QtCore.Qt.red)
            class_, score, x1, y1, x2, y2 = box
            w = x2-x1
            h = y2-y1
            p.drawRect(QtCore.QRect(QtCore.QPoint(x1, y1), QtCore.QSize(w, h)))
            p.drawText(x1, y1, "%s: %5.2f" % (labels[class_], score))
        p.end()
        pixmap2 = pixmap2.scaled(pixmap2.width()*2, pixmap2.height()*2)
        if self.rectified_pixmap == None:
            self.rectified_pixmap = self.scene.addPixmap(pixmap2)
            self.rectified_pixmap.setPos(QtCore.QPointF(3840 - pixmap2.width(), 2160-pixmap2.height()))
        else:
            self.rectified_pixmap.setPixmap(pixmap2)

    def analyzeBoxes(self, boxes):
        all_intersections = []
        for i in range(len(boxes)):
            first = boxes[i]
            first_rect = QtCore.QRectF(QtCore.QPointF(first[2], first[3]), QtCore.QPointF(first[4], first[5]))
            intersections = []
            for j in range(i+1, len(boxes)):
                second = boxes[j]
                second_rect = QtCore.QRectF(QtCore.QPointF(second[2], second[3]), QtCore.QPointF(second[4], second[5]))
                if first_rect.intersects(second_rect):
                    intersections.append((first, second))
            if intersections != []:
                all_intersections.append(intersections)

        nonoverlapping_boxes = set(boxes)
        if len(all_intersections):
            for intersections in all_intersections:
                for intersection in intersections:
                    first, second = intersection
                    if first[1] > second[1]:
                        if second in nonoverlapping_boxes:
                            nonoverlapping_boxes.remove(second)
                    else:
                        if first in nonoverlapping_boxes:
                            nonoverlapping_boxes.remove(first)

            boxes = nonoverlapping_boxes


            
        ordered_boxes = sorted(nonoverlapping_boxes, key=lambda x: boxCenter(x)[1])
        ordered_boxes_with_gaps = []
        for i in range(len(ordered_boxes)):
            box = ordered_boxes[i]
            bc = boxCenter(box[2:])
            ordered_boxes_with_gaps.append(box)
            if i < len(ordered_boxes) - 1:
                nextBox = ordered_boxes[i+1]
                dy = nextBox[3] - box[5]
                nbc = boxCenter(nextBox[2:])
                height = 50
                if dy > height:
                    pos = int(dy / height)
                    width = (((box[4] - box[2]) + (nextBox[4] - nextBox[2]))/2)/2
                    centerX = (box[4] + nextBox[2]) / 2
                    for j in range(1, pos):
                        currPosY = box[5] + ((height+5)*j)
                        newBox = (0, 1.0, centerX - width, currPosY - height/2, centerX + width, currPosY + height/2)
                        ordered_boxes_with_gaps.append(newBox)
                        if len(ordered_boxes_with_gaps) == 6:
                            break
            if len(ordered_boxes_with_gaps) == 6:
                break

        classes_ = [box[0] for box in ordered_boxes_with_gaps]
        while len(classes_) < 6:
            classes_.insert(0, 0)
            
        burger_renderer = BurgerRenderer(classes_, 720, 720, renderEmpty=True)
        image = burger_renderer.image
        image_128 = burger_renderer.image.scaled(128, 128).convertToFormat(QtGui.QImage.Format_RGB888)
        bits = image_128.constBits().asstring(128*128*3)
        img = np.fromstring(bits, dtype=np.uint8).reshape(128, 128, 3)
        pixmap3 = QtGui.QPixmap.fromImage(image)
        if self.burger_pixmap is None:
            self.burger_pixmap = self.scene.addPixmap(pixmap3)
            self.burger_pixmap.setPos(QtCore.QPointF(1370, 190))
        else:
            self.burger_pixmap.setPixmap(pixmap3)

        if len(classes_) != 6:
            print("Wrong size:", len(classes_))
            return None
        result = self.burger_classifier.classify(classes_)[0]
        if result[1] > 0.5:
            label = 'burger'
            self.label_text.setPlainText("BURGER")
            self.label_text.setPos(1500,1150)
            self.label_text.setDefaultTextColor(QtCore.Qt.green)
        else:
            label = 'notburger'
            self.label_text.setHtml("NOT<br>BURGER")
            self.label_text.setPos(1500,1150)
            self.label_text.setDefaultTextColor(QtCore.Qt.red)
        # self.image3_text.setText("P(burger) = %5.2f P(notburger) = %5.2f (%s" % (result[1], result[0], label))
        # label = label_burger(classes_)
        
        return ordered_boxes_with_gaps
        
    def camera(self):
        ret, img = self.cam.read()
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
                self.imageTo(image)
                self.imageTo2Clear()
                return
            else:
                short_ids = [id_[0] for id_ in ids]
                for i, corner in enumerate(corners):
                    d[short_ids[i]] = corner
                if len(d.keys()) != 4:
                    image = QtGui.QImage(img2.data, w3, h3, w3*3, QtGui.QImage.Format_RGB888).rgbSwapped()
                    self.imageTo(image)
                    self.imageTo2Clear()
                    return
                ul = d[0][0][0]
                ur = d[1][0][0]
                lr = d[2][0][0]
                ll = d[3][0][0]
                pts = np.array([ul, ur, lr, ll], np.int32)
                pts = pts.reshape((-1,1,2))
                cv2.polylines(img,[pts],True,(255,0,255))
                image = QtGui.QImage(img2.data, w3, h3, w3*3, QtGui.QImage.Format_RGB888).rgbSwapped()
                self.imageTo(image)

                orig_width = ur[0] - ul[0]
                orig_height = ll[1] - ul[1]
                # ratio = orig_width / float(orig_height)
                destCorners = np.array([ [0, 0], [WARPED_WIDTH, 0], [WARPED_WIDTH, WARPED_HEIGHT], [0, WARPED_HEIGHT]], dtype=np.float32)
                srcCorners = np.array([ul, ur, lr, ll], dtype=np.float32)
                pt = cv2.getPerspectiveTransform(srcCorners, destCorners)
                warped = cv2.warpPerspective(img, pt, (WARPED_WIDTH, WARPED_HEIGHT))
                cv2.imwrite("rectified/%05d.png" % self.counter, warped)
                expand = np.expand_dims(warped, axis=0)
                result = self.objdet.detect(expand)
                for i in range(result['num_detections']):
                    if result['detection_scores'][i] > 0.5:
                        class_ = result['detection_classes'][i]
                        box = result['detection_boxes'][i]
                        score = result['detection_scores'][i]
                        y1, x1 = box[0] * WARPED_HEIGHT, box[1] * WARPED_WIDTH
                        y2, x2 = box[2] * WARPED_HEIGHT, box[3] * WARPED_WIDTH
                        boxes.append((class_, score, x1, y1, x2, y2))
                warped_image = QtGui.QImage(warped.data, WARPED_WIDTH, WARPED_HEIGHT, 3*WARPED_WIDTH, QtGui.QImage.Format_RGB888).rgbSwapped()
                self.imageTo2(warped_image, boxes)
                self.counter += 1
        # else:
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
    # widget.show()
    widget.showFullScreen()
    app.exec_()
