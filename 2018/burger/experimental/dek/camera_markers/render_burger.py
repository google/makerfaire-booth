import numpy as np
import signal
import sys
from PyQt5 import QtGui, QtCore, QtSvg, QtWidgets
# from image_recognizer import ImageRecognizer

WIDTH=128
HEIGHT=128
SIZE=16
SIZE_HEIGHT=20
OFFSET=32

labels = {
    0: 'empty',
    1: 'topbun',
    2: 'lettuce',
    3: 'tomato',
    4: 'cheese',
    5: 'patty',
    6: 'bottombun'
    }

renderers = {}

for key, value in labels.items():
    if value == 'empty':
        renderers[value] = None
    else:
        renderers[value] = QtSvg.QSvgRenderer("../../../assets/%s.svg" % value)

class BurgerClassifier(object):
    def __init__(self, burger):
        image = QtGui.QImage(QtCore.QSize(WIDTH, HEIGHT), QtGui.QImage.Format_ARGB32)
        image.fill(QtGui.QColor(0, 0, 0, 0))
        painter = QtGui.QPainter(image)
        for i in range(len(burger)):
            layer = labels[burger[i]]
            bounds = QtCore.QRectF(OFFSET, (i-1)*SIZE_HEIGHT + 18, SIZE*4.4, SIZE*2.475)
            renderers[layer].render(painter, bounds)
        painter.end()

        self.image = image

if __name__ == '__main__':
    app = QtGui.QGuiApplication(sys.argv)
    b = BurgerClassifier([1,2,3,4,5,6])
    b.image.save("image.png")
