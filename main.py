import sys
import os

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from Tray import Sempy
from Wizard import SempyWizard


if __name__ == '__main__':
    app = QApplication(sys.argv)
    settings = QSettings(QSettings.IniFormat, QSettings.UserScope, "Sempy",  "config")

    if not os.path.exists(settings.fileName()):
        wizard = SempyWizard()
        wizard.show()

    w = QWidget()
    tray_icon = Sempy(parent=w, settings=settings)

    tray_icon.show()
    app.exec_()
