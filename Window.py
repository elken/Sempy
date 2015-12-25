from PyQt4.Qt import pyqtSlot
from PyQt4.QtCore import QSettings, Qt
from PyQt4.QtGui import *


# noinspection PyUnresolvedReferences
class SempyConfig(QDialog):

    def __init__(self):
        """
        Config window. Extremely messy atm, need to make this more functional.
        :return: A config window object
        """
        super(SempyConfig, self).__init__()
        self.info = {}
        self.settings = QSettings(QSettings.IniFormat, QSettings.UserScope, "Sempy", "config")

        self.reload_button = QPushButton("Reload")
        self.save_button = QPushButton("Save")
        self.refresh_button = QPushButton("Refresh")
        self.verify_button = QPushButton("Verify")

        self.box_layout = QGridLayout()
        self.main_layout = QGridLayout()
        self.box_group = QButtonGroup()
        self.btn_layout = QHBoxLayout()
        self.settings_layout = QGridLayout()

        self.interval_spinner = QSpinBox()
        self.interval_label = QLabel("Interval: ")
        self.token_box = QLineEdit()
        self.token_label = QLabel("API token: ")

        self.init_ui()

    def init_ui(self):
        """ Create all the UI elements """
        self.box_group.setExclusive(False)
        self.interval_spinner.setSuffix(" seconds")
        self.interval_spinner.setValue(int(self.settings.value("interval")))
        self.token_box.setText(self.settings.value("token"))
        self.setWindowTitle('Sempy Configuration')
        self.setWindowIcon(QIcon('res/semaphore.png'))
        self.interval_label.setBuddy(self.interval_spinner)
        self.box_layout.addWidget(QLabel("<b>Enable/disable repositories below:</b>"), 0, 0)
        row = 1

        self.settings.beginGroup("Repositories")
        for key in self.settings.allKeys():
            self.info[key] = self.settings.value(key)

        for key, val in self.info.items():
            checkbox = QCheckBox(key)
            if val == "True":
                checkbox.setCheckState(Qt.Checked)
            self.box_layout.addWidget(checkbox, row, 0)
            self.box_group.addButton(checkbox)
            row += 1
        self.settings.endGroup()

        self.save_button.clicked.connect(self.save)
        self.reload_button.clicked.connect(self.reload)
        self.verify_button.clicked.connect(self.verify)
        self.refresh_button.clicked.connect(self.refresh)
        self.btn_layout.addWidget(self.save_button)
        self.btn_layout.addWidget(self.reload_button)

        self.settings_layout.addWidget(self.interval_label, 0, 0)
        self.settings_layout.addWidget(self.interval_spinner, 0, 1)
        self.settings_layout.addWidget(self.token_label, 1, 0)
        self.settings_layout.addWidget(self.token_box, 1, 1)
        self.settings_layout.addWidget(self.refresh_button, 1, 2)
        self.settings_layout.addWidget(self.verify_button, 1, 3)

        self.main_layout.addItem(self.settings_layout, 0, 0)
        self.main_layout.addItem(self.box_layout, 2, 0)
        self.main_layout.addItem(self.btn_layout, 4, 0)

        self.setLayout(self.main_layout)

    @pyqtSlot()
    def save(self):
        self.settings.setValue("interval", self.interval_spinner.value())
        self.settings.setValue("token", self.token_box.text())
        self.settings.beginGroup("Repositories")
        for i in self.box_group.buttons():
            self.settings.setValue(i.text(), str(i.isChecked()).capitalize())
        self.settings.endGroup()

    @pyqtSlot()
    def reload(self):
        self.interval_spinner.setValue(int(self.settings.value("interval")))
        self.token_box.setText(self.settings.value("token"))
        for i in self.box_group.buttons():
            i.setCheckState(self.settings.value(i.text()))

    @pyqtSlot()
    def verify(self):
        print("Verify")

    @pyqtSlot()
    def refresh(self):
        print("refresh")

    def closeEvent(self, event):
        event.ignore()
        self.hide()
