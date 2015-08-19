import threading

from PyQt4 import QtGui

from Request import TeaTrayRequest


class TeaTray(QtGui.QSystemTrayIcon):

    def __init__(self, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, QtGui.QIcon("res/semaphore.png"), parent)
        self.menu = QtGui.QMenu(parent)

        threading.Timer(5, self.update_menu())

    def update_menu(self):
        tr = TeaTrayRequest()
        self.menu.clear()
        for i in tr.info.values():
            self.menu.addAction(QtGui.QIcon("res/" + i['result'] + ".svg"), i['owner'] + "/" + i['name'])

        self.menu.addSeparator()
        self.menu.addAction("Exit", QtGui.qApp.quit)
        self.setContextMenu(self.menu)
