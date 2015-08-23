import sys
import os

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from Tray import Sempy
from Wizard import SempyWizard

if __name__ == '__main__':
    app = QApplication(sys.argv)
    settings = QSettings(QSettings.IniFormat, QSettings.UserScope, "Sempy",  "config")

    # if not os.path.exists(settings.fileName()):
    wizard = SempyWizard()
    wizard.show()

    # if os.path.exists(settings.fileName()):
    #     w = QWidget()
    #     tray_icon = Sempy(w)
    #     tray_icon.show()

    sys.exit(app.exec_())
