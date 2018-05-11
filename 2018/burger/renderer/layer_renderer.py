import math
import numpy as np
import signal
import sys
from PyQt5 import QtGui, QtCore, QtSvg, QtWidgets

WIDTH=256
HEIGHT=256
ASPECT_RATIO = 1.85
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

def render_layer(layer, rot, tx, ty, scale):
    image = QtGui.QImage(QtCore.QSize(WIDTH, HEIGHT), QtGui.QImage.Format_ARGB32)
    image.fill(QtGui.QColor(0, 0, 0, 0))
    painter = QtGui.QPainter(image)
    renderer = renderers[layer]
    vertical_offset = renderer.viewBox().height()
    painter.translate(WIDTH/2, HEIGHT/2)
    painter.rotate(rot)
    painter.scale(scale, scale)
    painter.translate(-WIDTH/2, -HEIGHT/2)
    painter.translate(0, HEIGHT/ASPECT_RATIO/2)
    bounds = QtCore.QRectF(0, 0, WIDTH, HEIGHT/ASPECT_RATIO - vertical_offset/2.)
    renderers[layer].render(painter, bounds)
    painter.end()

    return image

def get_opaque_bbox(image):
    bits = image.constBits().asstring(image.width()*image.height()*4)
    img = np.fromstring(bits, dtype=np.uint8).reshape(image.width(), image.height(), 4)
    alpha = img[:, :, 3]
    x = np.where(alpha != 0)
    bbox = np.min(x[1]), np.min(x[0]), np.max(x[1]), np.max(x[0])
    return bbox


if __name__ == '__main__':
    app = QtGui.QGuiApplication(sys.argv)
    image = render_layer(labels[1], 0, 0, 0, 1)
    print get_opaque_bbox(image)
