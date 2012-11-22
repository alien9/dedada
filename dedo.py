import sys, re
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui, QtWebKit
from PyQt4.QtCore import Qt, SIGNAL, QEvent, QPoint, QSize, QUrl, QThread, QTimer, QPropertyAnimation, QRect,  QProcess,  SLOT
from finger import Ui_MainWindow
import Image;
from PyQt4.QtOpenGL import *
from OpenGL.GL import *
from OpenGL.GLU import *
from shader import ShaderProgram,ShaderCode

from multiprocessing import Process
class Rabisk(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.layers = []
        self.canvasWidth = 640 # size of image, not entire widget
        self.canvasHeight = 480
        self.initializeGL()
        
        self.setWindowState(Qt.WindowFullScreen)
        self.camera=QProcess(self)
        self.camera.readyReadStandardOutput.connect(self.handle_stdout)
        self.camera.start('python sense.py')
        
        
        
        
    def handle_stdout(self):
        byteArray=self.camera.readAllStandardOutput()
        data=re.sub(r'''\n+$''', "", byteArray.data())
        print data
        self.paintGL()
    def keyPressEvent(self, e):
        k=e.key()
        print e.key()
    def initializeGL(self):
        glClearColor(0.4, 0.4, 0.4, 1.0)

        # if a starting image, load it
#        if self.startImg is not None:
#            print(self.img.width())

        self.layers = [ Layer(self.canvasWidth,self.canvasHeight) ]
        self.strokeLayer = Layer(self.canvasWidth,self.canvasHeight)

        # if there's a starting image, draw it into the starting layer
        """
        if self.imgPath is not None:
            bottomLayer = self.layers[-1]
            bottomLayer.bind()

            # setup the orthographic projection and viewport
            glMatrixMode(GL_PROJECTION)
            glPushMatrix()
            glLoadIdentity()
            glOrtho(0, self.canvasWidth, 0, self.canvasHeight, -1, 1)
            glViewport(0, 0, self.canvasWidth, self.canvasHeight)
            

            imgTextureId = self.bindTexture(self.startImg, GL_TEXTURE_RECTANGLE_ARB)
            self.drawTexture(QPointF(0,0), imgTextureId, GL_TEXTURE_RECTANGLE_ARB)

            self.deleteTexture(imgTextureId)

            # restore the previous projection matrix and viewport
            glMatrixMode(GL_PROJECTION)
            glPopMatrix()
            glViewport(0, 0, self.width(), self.height()) # should be saved off?

            bottomLayer.release()

            self.startImg = None
        """
        # setup the necessary shaders
        self.program = ShaderProgram()
        self.program.attachShader(ShaderCode(GL_VERTEX_SHADER,'./shaders/basic.vert'))
        self.program.attachShader(ShaderCode(GL_FRAGMENT_SHADER,'./shaders/basic.frag'))
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)

        # draw FBO layers from the bottom up
        for layer in reversed(self.layers):
            self.drawTexture(QPointF(0,0), layer.texture(), GL_TEXTURE_RECTANGLE_ARB)

        # if stroke, draw to the stroke layer, draw stroke layer
        self.program.bind()
        glBegin(GL_QUADS)
        glVertex2f(10,10)
        glVertex2f(20,10)
        glVertex2f(20,20)
        glVertex2f(10,20)
        glEnd()
        self.program.release()
class Layer(QGLFramebufferObject):
    def __init__(self, width, height, target=GL_TEXTURE_RECTANGLE_ARB):
        QGLFramebufferObject.__init__(self, width, height, 
                                      QGLFramebufferObject.CombinedDepthStencil,
                                      target,
                                      GL_RGBA8)
app = QtGui.QApplication(sys.argv)
myapp = Rabisk() 
myapp.show()
sys.exit(app.exec_())
myapp.k.stop()
