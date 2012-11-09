import os
from PyQt4.QtCore import * 
from PyQt4.QtGui import *
from PyQt4 import uic
from PyQt4.QtOpenGL import *
from OpenGL.GL import *
from OpenGL.GLU import *

from shader import ShaderProgram,ShaderCode

class Canvas(QGLWidget):
    def __init__(self, imgPath=None):
        QGLWidget.__init__(self)

        self.layers = []
        self.canvasWidth = 640 # size of image, not entire widget
        self.canvasHeight = 480

        if imgPath is None:
            self.imgPath = None
            self.setWindowTitle('untitled*')
        else:
            if not os.path.exists(imgPath):
                raise IOError

            self.imgPath = imgPath
            self.startImg = QImage()
            self.startImg.load(self.imgPath)
            self.canvasWidth = self.startImg.width()
            self.canvasHeight = self.startImg.height()
            
            self.setWindowTitle(imgPath)

    def mousePressEvent(self, event):
        print('press')

    def mouseReleaseEvent(self, event):
        print('release')

    def mouseMoveEvent(self, event):
        print('move')

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
        

    def resizeGL(self, w, h):
        glViewport(0,0,w,h)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, w, 0, h, -1, 1)

    def initializeGL(self):
        glClearColor(0.4, 0.4, 0.4, 1.0)

        # if a starting image, load it
#        if self.startImg is not None:
#            print(self.img.width())

        self.layers = [ Layer(self.canvasWidth,self.canvasHeight) ]
        self.strokeLayer = Layer(self.canvasWidth,self.canvasHeight)

        # if there's a starting image, draw it into the starting layer
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

        # setup the necessary shaders
        self.program = ShaderProgram()
        self.program.attachShader(ShaderCode(GL_VERTEX_SHADER,'./shaders/basic.vert'))
        self.program.attachShader(ShaderCode(GL_FRAGMENT_SHADER,'./shaders/basic.frag'))

class Layer(QGLFramebufferObject):
    def __init__(self, width, height, target=GL_TEXTURE_RECTANGLE_ARB):
        QGLFramebufferObject.__init__(self, width, height, 
                                      QGLFramebufferObject.CombinedDepthStencil,
                                      target,
                                      GL_RGBA8)
