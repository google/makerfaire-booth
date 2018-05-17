import math
import numpy as np
import signal
import sys
from PyQt5 import QtGui, QtCore, QtSvg, QtWidgets
from burger_elements import BurgerElement
labels = {}
for layer, id_ in BurgerElement.__members__.items():
    labels[id_.value] = layer

WIDTH=256
HEIGHT=256
ASPECT_RATIO = 1.85

renderers = {}

for key, value in labels.items():
    if value == 'empty':
        renderers[value] = None
    else:
        renderers[value] = QtSvg.QSvgRenderer("../static/assets/%s.svg" % value)

def render_layer(layer, rot, tx, ty, scale, transparent=True):
    image = QtGui.QImage(QtCore.QSize(WIDTH, HEIGHT), QtGui.QImage.Format_ARGB32)
    if transparent:
        image.fill(QtGui.QColor(255, 255, 255, 0))
    else:
        image.fill(QtGui.QColor(255, 255, 255, 255))
    painter = QtGui.QPainter(image)
    renderer = renderers[layer]
    vertical_offset = renderer.viewBox().height()/2
    horizontal_offset = renderer.viewBox().width()/2
    painter.translate(WIDTH/2 - horizontal_offset, HEIGHT/2 - vertical_offset)
    painter.translate(horizontal_offset, vertical_offset)
    painter.rotate(rot)
    painter.translate(tx, ty)
    painter.scale(scale, scale)
    painter.translate(-horizontal_offset, -vertical_offset)
    bounds = QtCore.QRectF(renderer.viewBox())
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

def image_as_png(image):
    ba = QtCore.QByteArray()
    buf = QtCore.QBuffer(ba);
    buf.open(QtCore.QIODevice.WriteOnly);
    image.save(buf, "PNG")
    return ba.data()

if __name__ == '__main__':
    app = QtGui.QGuiApplication(sys.argv)
    image = render_layer(labels[1], 0, 0, 0, 1)
    image.save("image.png")
    bytes = image_as_png(image)
    open("test.png", "wb").write(bytes)
