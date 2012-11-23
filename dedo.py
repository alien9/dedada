import sys, re
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui, QtWebKit
from PyQt4.QtCore import Qt, SIGNAL, QEvent, QPoint, QSize, QUrl, QThread, QTimer, QPropertyAnimation, QRect,  QProcess,  SLOT
from finger import Ui_MainWindow
import Image;


from multiprocessing import Process
class Rabisk(QtGui.QMainWindow):
    text="peganingas"
    pic=None
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.layers = []
        self.canvasWidth = 640 # size of image, not entire widget
        self.canvasHeight = 480
        self.ui.label.setGeometry(QtCore.QRect(0, 0, 66, 17))
        print self.ui.centralwidget.width
        #self.ui.label.geometry.Width=self.ui.geometry.Width
        #self.ui.label.height=self.ui.height
        self.setWindowState(Qt.WindowFullScreen)
        print self.ui.centralwidget.width()
        self.ui.label.setGeometry(QtCore.QRect(0, 0, self.ui.centralwidget.width(), self.ui.centralwidget.height()))
        self.pic=QPixmap(self.ui.centralwidget.width(), self.ui.centralwidget.height())
        self.camera=QProcess(self)
        self.camera.readyReadStandardOutput.connect(self.handle_stdout)
        self.camera.start('python sense.py')
        self.show()
        
        
        
    def paintEvent(self, event):
        print "drawing"    
        qp=QtGui.QPainter()
        qp.begin(self)
        qp.setPen(QtGui.QColor(1,10,0))
        qp.drawText(10,10, self.text)
        qp.end()
        
        
    def handle_stdout(self):
        byteArray=self.camera.readAllStandardOutput()
        data=re.sub(r'''\n+$''', "", byteArray.data())
        print data
        self.text=data
        #self.ui.label.setText("whatever"+data);
        qp=QtGui.QPainter(self.pic)
        qp.setPen(QtGui.QColor(1,10,0))
        qp.drawText(100,10, self.text)
        self.ui.label.setPixmap(self.pic)
        

    def keyPressEvent(self, e):
        k=e.key()
        print e.key()

app = QtGui.QApplication(sys.argv)
myapp = Rabisk() 
myapp.show()
sys.exit(app.exec_())
myapp.k.stop()
