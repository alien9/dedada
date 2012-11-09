import sys, re
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui, QtWebKit
from PyQt4.QtCore import Qt, SIGNAL, QEvent, QPoint, QSize, QUrl, QThread, QTimer, QPropertyAnimation, QRect,  QProcess,  SLOT
from finger import Ui_MainWindow
import Image;
import cv;

from multiprocessing import Process
class Rabisk(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowState(Qt.WindowFullScreen)
        self.camera=QProcess(self)
        self.camera.readyReadStandardOutput.connect(self.handle_stdout)
        self.camera.start('python webcam.py')
    def handle_stdout(self):
        byteArray=self.camera.readAllStandardOutput()
        self.data+=re.sub(r'''\n+$''', "", byteArray.data())
        print "mih"
    def keyPressEvent(self, e):
        k=e.key()
        print e.key()

app = QtGui.QApplication(sys.argv)
myapp = Rabisk() 
myapp.show()
sys.exit(app.exec_())
myapp.k.stop()
