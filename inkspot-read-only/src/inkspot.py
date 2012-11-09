import sys, signal
import getopt
from PyQt4.QtCore import * 
from PyQt4.QtGui import *
from PyQt4 import uic 

from canvas import Canvas

class Inkspot(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.ui = uic.loadUi("./ui/inkspot.ui")
        self.ui.show()

        self.canvases = []
        self.canvases.append(Canvas("NightCrawler.jpg"))
        self.canvases[0].show()

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
        except getopt.error, msg:
             raise Usage(msg)

        app = QApplication(sys.argv)
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        window = Inkspot()
        return app.exec_()
#        app.setMainWidget(window)
#        app.exec_loop()

    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())
