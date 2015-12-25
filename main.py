import sys
from multiprocessing import Process
from os import path

from PyQt4 import QtCore, QtGui

from Sempy import Sempy
from Wizard import SempyWizard


def run_wizard():
    app = QtGui.QApplication(sys.argv)
    wizard = SempyWizard()
    wizard.show()
    app.exec_()

if __name__ == '__main__':
    # noinspection PyTypeChecker,PyArgumentList
    QtCore.QCoreApplication.addLibraryPath(path.join(path.dirname(QtCore.__file__), "plugins"))
    app = QtGui.QApplication(sys.argv)
    settings = QtCore.QSettings(QtCore.QSettings.IniFormat, QtCore.QSettings.UserScope, "Sempy", "config")

    print(settings.fileName())
    if not path.exists(settings.fileName()):
        t = Process(target=run_wizard)
        t.start()
        t.join()

    w = QtGui.QWidget()
    tray_icon = Sempy(w)

    tray_icon.show()
    sys.exit(app.exec_())
