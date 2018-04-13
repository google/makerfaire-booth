import numpy
import signal
import sys
from PySide import QtGui, QtCore, QtSvg
import cv2

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
        patty = QtSvg.QGraphicsSvgItem("../../../assets/patty.svg")
        patty.setFlags(QtGui.QGraphicsItem.ItemIsMovable)
        self.scene.addItem(patty)

        self.image_widget = QtGui.QLabel(self)
        self.image_widget.setFixedSize(1024,768)

        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.view)
        self.layout.addWidget(self.image_widget)
        self.setLayout(self.layout)

    def changed(self):
        image = QtGui.QImage(QtCore.QSize(1024, 768), QtGui.QImage.Format_RGB888)
        image.fill(QtCore.Qt.white)

        painter = QtGui.QPainter(image)
        self.scene.render(painter)
        painter.end()
        bits = image.constBits()
        img = numpy.fromstring(image.constBits(), dtype=numpy.uint8).reshape(768, 1024, 3)
        cv2.imwrite("test.png", img)
        edged = cv2.Canny(img, 40, 200)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
        im2, contours, hierarchy = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        for c in contours:
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.02 * peri, True)
                cv2.drawContours(img, [approx], -1, (0, 255, 0), 1)


        image = QtGui.QImage(img.data, 1024, 768, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(image)
        self.image_widget.setPixmap(pixmap)
        
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtGui.QApplication(sys.argv)
        
    widget = Widget()
    widget.show()
    
    app.exec_()
