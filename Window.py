from PyQt4.Qt import pyqtSlot
from PyQt4.QtCore import QSettings
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
        self.refresh_button = QPushButton("Refresh repos")
        self.verify_button = QPushButton("Verify")

        self.box_layout = QGridLayout()
        self.main_layout = QGridLayout()
        self.box_group = QButtonGroup()
        self.btn_layout = QHBoxLayout()

        self.interval_spinner = QSpinBox()
        self.interval_label = QLabel("Interval: ")
        self.token_box = QLineEdit()
        self.token_label = QLabel("API token: ")

        self.init_ui()

    def init_ui(self):
        self.box_group.setExclusive(False)
        self.interval_spinner.setSuffix(" seconds")
        self.interval_spinner.setValue(int(self.settings.value("interval")))
        self.token_box.setText(self.settings.value("token"))
        self.setWindowTitle('Sempy Configuration')
        self.setWindowIcon(QIcon('res/semaphore.png'))
        self.interval_label.setBuddy(self.interval_spinner)
        row = 0
        self.settings.beginGroup("Repositories")
        for key in self.settings.allKeys():
            self.info[key] = self.settings.value(key)

        for key, val in self.info.items():
            checkbox = QCheckBox(key, self)
            self.box_layout.addWidget(checkbox, row, 0)
            self.box_group.addButton(checkbox)
            label = QLabel()
            # icon = QIcon("res/" + val['result'] + ".svg")
            icon = QIcon("res/passed.svg")
            label.setPixmap(icon.pixmap(8))
            self.box_layout.addWidget(label, row, 1)
            row += 1

        self.save_button.clicked.connect(self.save)
        self.reload_button.clicked.connect(self.reload)
        self.verify_button.clicked.connect(self.verify)
        self.refresh_button.clicked.connect(self.refresh)
        self.btn_layout.addWidget(self.save_button)
        self.btn_layout.addWidget(self.reload_button)

        self.main_layout.addWidget(self.interval_label, 0, 0)
        self.main_layout.addWidget(self.interval_spinner, 0, 1)
        self.main_layout.addWidget(self.token_label, 1, 0)
        self.main_layout.addWidget(self.token_box, 1, 1)
        self.main_layout.addWidget(self.refresh_button, 1, 2)
        self.main_layout.addWidget(self.verify_button, 1, 3)
        self.main_layout.addWidget(QLabel("<b>Enable/disable repositories below:</b>"), 2, 0)
        self.main_layout.addItem(self.box_layout, 3, 0)
        # self.main_layout.addItem(self.btn_layout, 4, 0)
        self.main_layout.addWidget(self.save_button, 4, 0)
        self.main_layout.addWidget(self.reload_button, 4, 1)
        self.setLayout(self.main_layout)

    @pyqtSlot()
    def save(self):
        print("save")

    @pyqtSlot()
    def reload(self):
        print("reload")

    @pyqtSlot()
    def verify(self):
        print("Verify")

    @pyqtSlot()
    def refresh(self):
        print("refresh")

    def closeEvent(self, event):
        event.ignore()
        self.hide()
