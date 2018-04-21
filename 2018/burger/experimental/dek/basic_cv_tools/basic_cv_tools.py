import numpy as np
import signal
import sys
from PyQt5 import QtGui, QtCore, QtSvg, QtWidgets
from canny import canny

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
        item.setScale(1.5)
        rect = item.boundingRect()
        newPos = self.mapToScene(e.pos())# - QtCore.QPoint(rect.bottomRight()))
        print newPos
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
        self.view = QGraphicsView(self.scene)
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
        self.icons.setFixedSize(128, 6*64)
        self.iconsLayout = QtWidgets.QVBoxLayout()
        self.icons.setLayout(self.iconsLayout)
        
        self.topbun = QSvgWidget("../../../assets/topbun.svg")
        self.lettuce = QSvgWidget("../../../assets/lettuce.svg")
        self.tomato = QSvgWidget("../../../assets/tomato.svg")
        self.cheese = QSvgWidget("../../../assets/cheese.svg")
        self.patty = QSvgWidget("../../../assets/patty.svg")
        self.bottombun = QSvgWidget("../../../assets/bottombun.svg")
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
        self.layout.addWidget(self.image_widget)
        self.setLayout(self.layout)

        
    def topbun_clicked(self, *args):
        print args
        
    def buttonAClicked(self, *args):
        print args
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
        image = canny(img)
        pixmap = QtGui.QPixmap.fromImage(image)
        self.image_widget.setPixmap(pixmap)
        
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtWidgets.QApplication(sys.argv)
        
    widget = Widget()
    widget.show()
    
    app.exec_()
