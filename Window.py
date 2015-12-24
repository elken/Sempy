from PyQt4 import QtGui


class SempyConfig(QtGui.QWidget):

    def __init__(self):
        super(SempyConfig, self).__init__()
        self.initUi()

    def initUi(self):
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Sempy Configuration')
        self.setWindowIcon(QtGui.QIcon('res/semaphore.png'))
