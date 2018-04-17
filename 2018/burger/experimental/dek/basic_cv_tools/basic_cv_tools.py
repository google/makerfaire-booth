import numpy as np
import signal
import sys
from PySide import QtGui, QtCore, QtSvg
from canny import canny
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

class QGraphicsPixmapItem(QtGui.QGraphicsPixmapItem):
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

class Widget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.scene = QtGui.QGraphicsScene()
        self.scene.setSceneRect(0, 0, 1024, 768)
        self.scene.changed.connect(self.changed)
        self.view = QtGui.QGraphicsView(self.scene)
        self.view.setFixedSize(1024,768)
        self.view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
	self.view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.view.setMouseTracking(True)
        topbun_webcam = QGraphicsPixmapItem("/home/dek/Downloads/my_photo-1-crop.jpg")
        topbun_webcam.setFlags(QtGui.QGraphicsItem.ItemIsMovable)
        # lettuce = QGraphicsSvgItem("../../../assets/topbun.svg")
        # lettuce.setFlags(QtGui.QGraphicsItem.ItemIsMovable)
        # lettuce.setScale(2)
        self.scene.addItem(topbun_webcam)

        self.image_widget = QtGui.QLabel(self)
        self.image_widget.setFixedSize(1024,768)

        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.view)
        self.layout.addWidget(self.image_widget)
        self.setLayout(self.layout)
        self.objdet = ObjectDetector()
        

    def changed(self):
        image = QtGui.QImage(QtCore.QSize(1024, 768), QtGui.QImage.Format_RGB888)
        image.fill(QtCore.Qt.white)

        painter = QtGui.QPainter(image)
        self.scene.render(painter)
        painter.end()
        bits = image.constBits()
        img = np.fromstring(image.constBits(), dtype=np.uint8).reshape(768, 1024, 3)
        # image = canny(img)

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
    app = QtGui.QApplication(sys.argv)
        
    widget = Widget()
    widget.show()
    
    app.exec_()
