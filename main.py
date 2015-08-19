__author__ = 'elken'

import sys

from PyQt4 import QtGui

from TeaTray import TeaTray


def main():
    app = QtGui.QApplication(sys.argv)

    w = QtGui.QWidget()
    trayIcon = TeaTray.TeaTray(w)

    trayIcon.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
