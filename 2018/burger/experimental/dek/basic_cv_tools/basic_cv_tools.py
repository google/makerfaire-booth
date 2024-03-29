import numpy as np
import signal
import sys
from PyQt5 import QtGui, QtCore, QtSvg, QtWidgets
from canny import canny
from object_detector import ObjectDetector
sys.path.insert(0, "../../../constants")
from burger_elements import BurgerElement

WIDTH=1280
HEIGHT=720

labels = dict([(member.value, member.name) for member in BurgerElement.__members__.values()])

class QGraphicsSvgItem(QtSvg.QGraphicsSvgItem):
    def __init__(self, *args, **kwargs):
        super(QGraphicsSvgItem, self).__init__(*args, **kwargs)

    def mouseMoveEvent(self, event):
        if (event.buttons() & QtCore.Qt.LeftButton):
            if event.modifiers() & QtCore.Qt.ControlModifier:
                delta = event.scenePos() - event.buttonDownScenePos(QtCore.Qt.LeftButton)
                scale = self.scale() + delta.x()/50
                if scale > 0:
                    self.setScale(scale)
                return
            elif event.modifiers() & QtCore.Qt.ShiftModifier:
                delta = event.scenePos() - event.buttonDownScenePos(QtCore.Qt.LeftButton)
                self.setRotation(delta.x())
                return
        return super(QGraphicsSvgItem, self).mouseMoveEvent(event)

    def mousePressEvent(self, event):
        if (event.buttons() & QtCore.Qt.LeftButton):
            if event.modifiers() & QtCore.Qt.ControlModifier or \
               event.modifiers() & QtCore.Qt.ShiftModifier:
                return
        
        return super(QGraphicsSvgItem, self).mousePressEvent(event)

class QGraphicsPixmapItem(QtWidgets.QGraphicsPixmapItem):
    def __init__(self, *args, **kwargs):
        super(QGraphicsPixmapItem, self).__init__(*args, **kwargs)

        
    def mouseMoveEvent(self, event):
        if (event.buttons() & QtCore.Qt.LeftButton) and event.modifiers() & QtCore.Qt.ControlModifier:
            delta = event.scenePos() - event.buttonDownScenePos(QtCore.Qt.LeftButton)
            
            scale = self.scale() + delta.x()/50
            if scale > 0:
                self.setScale(scale)
            return
        return super(QGraphicsPixmapItem, self).mouseMoveEvent(event)

    def mousePressEvent(self, event):
        if (event.buttons() & QtCore.Qt.LeftButton) and event.modifiers() & QtCore.Qt.ControlModifier:
            return
        
        return super(QGraphicsPixmapItem, self).mousePressEvent(event)

class QGraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, *args, **kwargs):
        super(QGraphicsView, self).__init__(*args, **kwargs)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore() 

    def dragMoveEvent(self, e):
        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore() 

    def dropEvent(self, e):
        path = e.mimeData().text()
        item = QGraphicsSvgItem(path)
        item.setFlags(QtWidgets.QGraphicsItem.ItemIsMovable)
        item.setScale(1)
        rect = item.boundingRect()
        newPos = self.mapToScene(e.pos())# - QtCore.QPoint(rect.bottomRight()))
        item.setPos(newPos)
        self.scene().addItem(item)

class QSvgWidget(QtSvg.QSvgWidget):
    def __init__(self, *args, **kwargs):
        self.path = args[0]
        super(QSvgWidget, self).__init__(*args, **kwargs)
        
    def mousePressEvent(self, event):
        if (event.buttons() & QtCore.Qt.LeftButton):
            mimeData = QtCore.QMimeData()
            mimeData.setText(self.path)
            drag = QtGui.QDrag(self)
            image = QtGui.QImage(self.sizeHint(), QtGui.QImage.Format_RGB888)
            image.fill(QtCore.Qt.white)
            painter = QtGui.QPainter(image)
            self.render(painter)
            painter.end()
            pixmap = QtGui.QPixmap(self.sizeHint())
            pixmap.convertFromImage(image)
            drag.setPixmap(pixmap)
            drag.setMimeData(mimeData)
            dropAction = drag.exec_(QtCore.Qt.MoveAction)
            return
        
        return super(QSvgWidget, self).mousePressEvent(event)


class Widget(QtWidgets.QWidget):
    def __init__(self):
        super(Widget, self).__init__()

        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setSceneRect(0, 0, WIDTH, HEIGHT)
        self.scene.changed.connect(self.changed)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.classify)
        self.timer.start(250) 

        self.view = QGraphicsView(self.scene)
        self.view.setFixedSize(WIDTH,HEIGHT)
        self.view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.view.setMouseTracking(True)
        # pixmap = QtGui.QPixmap("my_photo-1-crop.jpg")
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
        self.icons.setFixedSize(128, 6*64)
        self.iconsLayout = QtWidgets.QVBoxLayout()
        self.icons.setLayout(self.iconsLayout)
        
        self.topbun = QSvgWidget("../../../static/assets/topbun.svg")
        self.lettuce = QSvgWidget("../../../static/assets/lettuce.svg")
        self.tomato = QSvgWidget("../../../static/assets/tomato.svg")
        self.cheese = QSvgWidget("../../../static/assets/cheese.svg")
        self.patty = QSvgWidget("../../../static/assets/patty.svg")
        self.bottombun = QSvgWidget("../../../static/assets/bottombun.svg")
        self.banana = QSvgWidget("../../../static/assets/banana.svg")
        self.book = QSvgWidget("../../../static/assets/book.svg")
        self.shoe = QSvgWidget("../../../static/assets/shoe.svg")
        self.iconsLayout.addWidget(self.topbun)
        self.iconsLayout.addWidget(self.lettuce)
        self.iconsLayout.addWidget(self.tomato)
        self.iconsLayout.addWidget(self.cheese)
        self.iconsLayout.addWidget(self.patty)
        self.iconsLayout.addWidget(self.bottombun)
        self.iconsLayout.addWidget(self.banana)
        self.iconsLayout.addWidget(self.book)
        self.iconsLayout.addWidget(self.shoe)

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
        self.layout.addWidget(self.image_widget)
        self.setLayout(self.layout)

        self.objdet = ObjectDetector()
        
    def topbun_clicked(self, *args):
        print(args)
        
    def buttonAClicked(self, *args):
        self.classify()
        
    def changed(self):
        self.classify()
        
    def classify(self):
        image = QtGui.QImage(QtCore.QSize(WIDTH, HEIGHT), QtGui.QImage.Format_RGB888)
        image.fill(QtCore.Qt.white)
        painter = QtGui.QPainter(image)
        self.scene.render(painter)
        painter.end()
        bits = image.constBits().asstring(HEIGHT*WIDTH*3)
        img = np.fromstring(bits, dtype=np.uint8).reshape(HEIGHT, WIDTH, 3)
        # image = canny(img)

        expand = np.expand_dims(img, axis=0)
        result = self.objdet.detect(expand)
        boxes = []
        for i in range(result['num_detections']):
            if result['detection_scores'][i] > 0.4:
                class_ = result['detection_classes'][i]
                box = result['detection_boxes'][i]
                score = result['detection_scores'][i]
                y1, x1 = box[0] * HEIGHT, box[1] * WIDTH
                y2, x2 = box[2] * HEIGHT, box[3] * WIDTH
                boxes.append((class_, score, x1, y1, x2, y2))
        
        pixmap = QtGui.QPixmap.fromImage(image)
        p = QtGui.QPainter()
        p.begin(pixmap)
        for box in boxes:
            p.setPen(QtCore.Qt.red)
            class_, score, x1, y1, x2, y2 = box
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
