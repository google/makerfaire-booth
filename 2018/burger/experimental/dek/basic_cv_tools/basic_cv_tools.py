import numpy as np
import signal
import sys
#from PySide import QtGui, QtCore, QtSvg
from PyQt5 import QtGui, QtCore, QtSvg, QtWidgets
#from canny import canny
# from object_detector import ObjectDetector

WIDTH=640
HEIGHT=480

labels = {
    0: 'empty',
    1: 'topbun',
    2: 'lettuce',
    3: 'tomato',
    4: 'cheese',
    5: 'patty',
    6: 'bottombun'
    }

class QGraphicsSvgItem(QtSvg.QGraphicsSvgItem):
    def __init__(self, *args, **kwargs):
        super(QGraphicsSvgItem, self).__init__(*args, **kwargs)

        self.press = None
        
    def mouseMoveEvent(self, event):
        if (event.buttons() & QtCore.Qt.LeftButton) and event.modifiers() & QtCore.Qt.ControlModifier:
            delta = event.scenePos() - self.press
            
            scale = self.scale() + delta.x()/50
            if scale > 0:
                self.setScale(scale)
            return
        return super(QGraphicsSvgItem, self).mouseMoveEvent(event)

    def mousePressEvent(self, event):
        if (event.buttons() & QtCore.Qt.LeftButton) and event.modifiers() & QtCore.Qt.ControlModifier:
            print "blah press", event.scenePos()
            self.press = event.scenePos()
            return
        
        return super(QGraphicsSvgItem, self).mousePressEvent(event)

class QGraphicsPixmapItem(QtWidgets.QGraphicsPixmapItem):
    def __init__(self, *args, **kwargs):
        super(QGraphicsPixmapItem, self).__init__(*args, **kwargs)

        self.press = None
        
    def mouseMoveEvent(self, event):
        if (event.buttons() & QtCore.Qt.LeftButton) and event.modifiers() & QtCore.Qt.ControlModifier:
            delta = event.scenePos() - self.press
            
            scale = self.scale() + delta.x()/50
            if scale > 0:
                self.setScale(scale)
            return
        return super(QGraphicsPixmapItem, self).mouseMoveEvent(event)

    def mousePressEvent(self, event):
        if (event.buttons() & QtCore.Qt.LeftButton) and event.modifiers() & QtCore.Qt.ControlModifier:
            print "blah press", event.scenePos()
            self.press = event.scenePos()
            return
        
        return super(QGraphicsPixmapItem, self).mousePressEvent(event)

class Widget(QtWidgets.QWidget):
    def __init__(self):
        super(Widget, self).__init__()

        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setSceneRect(0, 0, WIDTH, HEIGHT)
        self.scene.changed.connect(self.changed)
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.view.setFixedSize(WIDTH,HEIGHT)
        self.view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
	self.view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.view.setMouseTracking(True)
        pixmap = QtGui.QPixmap("my_photo-1-crop.jpg")
        # topbun_webcam = QGraphicsPixmapItem(pixmap)
        # topbun_webcam.setFlags(QtWidgets.QGraphicsItem.ItemIsMovable)
        # topbun_webcam.setScale(2)
        # self.scene.addItem(topbun_webcam)

        # lettuce = QGraphicsSvgItem("../../../assets/lettuce.svg")
        # lettuce.setFlags(QtWidgets.QGraphicsItem.ItemIsMovable)
        # lettuce.setScale(2)
        # self.scene.addItem(lettuce)

        self.image_widget = QtWidgets.QLabel(self)
        self.image_widget.setFixedSize(WIDTH,HEIGHT)

        self.icons = QtWidgets.QWidget(self)
        self.iconsLayout = QtWidgets.QVBoxLayout()
        self.icons.setLayout(self.iconsLayout)
        self.topbun = QtSvg.QSvgWidget("../../../assets/topbun.svg")
        self.lettuce = QtSvg.QSvgWidget("../../../assets/lettuce.svg")
        self.tomato = QtSvg.QSvgWidget("../../../assets/tomato.svg")
        self.cheese = QtSvg.QSvgWidget("../../../assets/cheese.svg")
        self.patty = QtSvg.QSvgWidget("../../../assets/patty.svg")
        self.bottombun = QtSvg.QSvgWidget("../../../assets/bottombun.svg")
        self.iconsLayout.addWidget(self.topbun)
        self.iconsLayout.addWidget(self.lettuce)
        self.iconsLayout.addWidget(self.tomato)
        self.iconsLayout.addWidget(self.cheese)
        self.iconsLayout.addWidget(self.patty)
        self.iconsLayout.addWidget(self.bottombun)

        self.buttons = QtWidgets.QWidget(self)
        self.buttonsLayout = QtWidgets.QHBoxLayout()
        self.buttons.setLayout(self.buttonsLayout)
        self.buttonA = QtWidgets.QPushButton("Classify")
        self.buttonA.clicked.connect(self.buttonAClicked)
        self.buttonsLayout.addWidget(self.buttonA)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(self.icons)
        # self.layout.addWidget(self.buttons)
        self.layout.addWidget(self.view)
        # self.layout.addWidget(self.image_widget)
        self.setLayout(self.layout)

        # self.objdet = ObjectDetector()
        

    def buttonAClicked(self, *args):
        print args
        self.classify()
        
    def changed(self):
        pass
        # self.classify()
        
    def classify(self):
        image = QtGui.QImage(QtCore.QSize(WIDTH, HEIGHT), QtGui.QImage.Format_RGB888)
        image.fill(QtCore.Qt.white)

        painter = QtGui.QPainter(image)
        self.scene.render(painter)
        painter.end()
        bits = image.constBits().asstring(HEIGHT*WIDTH*3)
        img = np.fromstring(bits, dtype=np.uint8).reshape(HEIGHT, WIDTH, 3)
        # ret = canny(img)        
        # image = QtGui.QImage(ret.data, WIDTH, HEIGHT, QtGui.QImage.Format_RGB888)

        h, w, _ = img.shape
        
        expand = np.expand_dims(img, axis=0)
        result = self.objdet.detect(expand)
        boxes = []
        for i in range(result['num_detections']):
            if result['detection_scores'][i] > 0.4:
                class_ = result['detection_classes'][i]
                box = result['detection_boxes'][i]
                score = result['detection_scores'][i]
                y1, x1 = box[0] * h, box[1] * w
                y2, x2 = box[2] * h, box[3] * w
                boxes.append((class_, score, x1, y1, x2, y2))

        image = QtGui.QImage(img.data, w, h, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(image)
        p = QtGui.QPainter()
        p.begin(pixmap)
        for item in boxes:
            p.setPen(QtCore.Qt.red)
            class_, score, x1, y1, x2, y2 = item
            w = x2-x1
            h = y2-y1
            p.drawRect(x1, y1, w, h)
            p.drawText(x1, y1, "%s: %5.2f" % (labels[class_], score))
        p.end ()
        
        self.image_widget.setPixmap(pixmap)
        
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtWidgets.QApplication(sys.argv)
        
    widget = Widget()
    widget.show()
    
    app.exec_()
