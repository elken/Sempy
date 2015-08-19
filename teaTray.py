__author__ = 'elken'

#!/usr/bin/env python
import sys
from PyQt4 import QtGui


class TeaTray(QtGui.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtGui.QMenu(parent)
        passedAction = menu.addAction("Passed")
        failedAction = menu.addAction("Failed")
        runningAction = menu.addAction("Running")
        menu.addSeparator()
        exitAction = menu.addAction("Exit", QtGui.qApp.quit)
        passedAction.setIcon(QtGui.QIcon("res/pass.svg"))
        failedAction.setIcon(QtGui.QIcon("res/fail.svg"))
        runningAction.setIcon(QtGui.QIcon("res/running.svg"))
        self.setContextMenu(menu)


def main():
    app = QtGui.QApplication(sys.argv)

    w = QtGui.QWidget()
    trayIcon = TeaTray(QtGui.QIcon("res/pass.svg"), w)

    trayIcon.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
