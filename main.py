import sys
import os
from multiprocessing import Process

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from Sempy import Sempy
from Wizard import SempyWizard


def run_wizard():
    app = QApplication(sys.argv)
    wizard = SempyWizard()
    wizard.show()
    app.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    settings = QSettings(QSettings.IniFormat, QSettings.UserScope, "Sempy",  "config")

    print(settings.fileName())
    if not os.path.exists(settings.fileName()):
        t = Process(target=run_wizard)
        t.start()
        t.join()

    w = QWidget()
    tray_icon = Sempy(w)

    tray_icon.show()
    sys.exit(app.exec_())
