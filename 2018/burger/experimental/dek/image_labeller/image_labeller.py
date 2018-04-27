import sys
import signal
from PyQt5 import QtGui, QtCore, QtWidgets

NO_STATE=0
MOVE=1
RESIZE=2
class QGraphicsRectItem(QtWidgets.QGraphicsRectItem):
    def __init__(self, *args, **kwargs):
        super(QGraphicsRectItem, self).__init__(*args, **kwargs)
        self.setFlags(QtWidgets.QGraphicsItem.ItemIsMovable | QtWidgets.QGraphicsItem.ItemSendsGeometryChanges)
        self.start = None
        self.end = None
        self.state = NO_STATE
        
    def mousePressEvent(self, event):
        print "item press", event.scenePos()
        if QtGui.QVector2D(event.scenePos() - self.sceneBoundingRect().bottomRight()).length() < 10:
            self.state = RESIZE
            self.start = event.scenePos()
        else:
            self.state = MOVE
        super(QGraphicsRectItem, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.state == RESIZE:
            sp = event.scenePos()
            d = sp - self.start
            r = self.rect()
            r.setBottomRight(sp)
            self.setRect(r)
            self.start = event.scenePos()
            event.ignore()
        else:
            super(QGraphicsRectItem, self).mouseMoveEvent(event)
        
    def mouseReleaseEvent(self, event):
        print "item release"
        self.end = event.scenePos()
        self.state = NO_STATE
        super(QGraphicsRectItem, self).mouseReleaseEvent(event)
        
class QGraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, *args, **kwargs):
        super(QGraphicsView, self).__init__(*args, **kwargs)
        self.start = None

class QGraphicsScene(QtWidgets.QGraphicsScene):
    def __init__(self, *args, **kwargs):
        super(QGraphicsScene, self).__init__(*args, **kwargs)
        self.start = None
        
    def mousePressEvent(self, event):
        print "blah press", event.scenePos()
        self.start = event.scenePos()
        super(QGraphicsScene, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        print "blah release", event.scenePos()
        if self.mouseGrabberItem():
            print "there is a mouse grabber, not adding!"
        else:
            end = event.scenePos()
            print self.start, end
            r = QtCore.QRectF(self.start, end)
            print r
            self.addItem(QGraphicsRectItem(r))
            self.start = None
        super(QGraphicsScene, self).mouseReleaseEvent(event)
        
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.central_widget = QtWidgets.QWidget(self)
        central_layout = QtWidgets.QVBoxLayout()
        self.central_widget.setLayout(central_layout)
        self.setCentralWidget(self.central_widget)

        self.view = QGraphicsView()
        self.view.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)

        self.control_widget = QtWidgets.QWidget(self)
        self.forward_button = QtWidgets.QLabel()
        self.backward_button = QtWidgets.QLabel()
        image = QtGui.QImage("play.png", 'ARGB32')
        pixmap = QtGui.QPixmap(image)
        self.forward_button.setPixmap(pixmap)
        self.backward_button.setPixmap(pixmap)
        self.control_layout = QtWidgets.QHBoxLayout()
        self.control_layout.addWidget(self.forward_button)
        self.control_layout.addWidget(self.backward_button)
        self.control_widget.setLayout(self.control_layout)

        central_layout.addWidget(self.view)
        central_layout.addWidget(self.control_widget)


        exitAction = QtWidgets.QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtWidgets.qApp.quit)
        loadImageAction = QtWidgets.QAction(QtGui.QIcon('loadImage.png'), '&Load Image', self)
        loadImageAction.setStatusTip('LoadImage')
        loadImageAction.triggered.connect(self.loadImage)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(loadImageAction)
        fileMenu.addAction(exitAction)

        self.loadImage("images/00001.png")

    def loadImage(self, filename=None):
        if not filename:
            filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')[0]
        image = QtGui.QImage(filename, 'ARGB32')
        pixmap = QtGui.QPixmap(image)
        image_item = self.scene.addPixmap(pixmap)
        self.scene.setSceneRect(QtCore.QRectF(pixmap.rect()))

    def loadMovie(self):
        pass
    
    
if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtWidgets.QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    app.exec_()
