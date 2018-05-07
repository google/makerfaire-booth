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
        renderers[value] = QtSvg.QSvgRenderer("../assets/%s.svg" % value)

class BurgerRenderer(object):
    def __init__(self, burger, width, height):
        image = QtGui.QImage(QtCore.QSize(width, height), QtGui.QImage.Format_ARGB32)
        image.fill(QtGui.QColor(0, 0, 0, 0))
        painter = QtGui.QPainter(image)
        if len(burger) < 6:
            empty_len = 6-len(burger)
            for _ in range(empty_len):
                burger.insert(0, 0)
        for i in range(len(burger)):
            layer_idx = burger[i]
            if layer_idx != 0:

                layer = labels[layer_idx]
                ratio = (width/float(WIDTH))
                bounds = QtCore.QRectF(OFFSET * ratio, (i-1)*SIZE_HEIGHT*ratio + 18*ratio, SIZE*4.4*ratio, SIZE*2.475*ratio)
                renderers[layer].render(painter, bounds)
        painter.end()

        self.image = image

if __name__ == '__main__':
    app = QtGui.QGuiApplication(sys.argv)
    b = BurgerRenderer([1,2,3,4,5,6], 128, 128)
    b.image.save("image.png")
