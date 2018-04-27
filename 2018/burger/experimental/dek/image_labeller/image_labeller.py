import sys
import signal
from PyQt5 import QtGui, QtCore, QtWidgets

class QGraphicsRectItem(QtWidgets.QGraphicsRectItem):
    def __init__(self, *args, **kwargs):
        super(QGraphicsRectItem, self).__init__(*args, **kwargs)

    def mousePressEvent(self, event):
        print "item press"
        event.accept()
    
class QGraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, *args, **kwargs):
        super(QGraphicsView, self).__init__(*args, **kwargs)
        self.start = None
        
    def mousePressEvent(self, event):
        print "view press"
        self.start = event.pos()

        super(QGraphicsView, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        end = event.pos()
        if self.start:
            r = QGraphicsRectItem(QtCore.QRectF(self.start, end))
            self.start = None
            self.scene().addItem(r)
        else:
            print "missing start"
        
        super(QGraphicsView, self).mouseReleaseEvent(event)
        
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.central_widget = QtWidgets.QWidget(self)
        central_layout = QtWidgets.QVBoxLayout()
        self.central_widget.setLayout(central_layout)
        self.setCentralWidget(self.central_widget)

        self.view = QGraphicsView()
        self.view.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)
        self.scene = QtWidgets.QGraphicsScene()
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
