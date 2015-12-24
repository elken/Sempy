from PyQt4.QtCore import QSettings
from PyQt4.QtGui import *


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
        self.key_button = QPushButton("Refresh repos")

        self.box_layout = QGridLayout()
        self.main_layout = QGridLayout()
        self.box_group = QButtonGroup()
        self.btn_layout = QHBoxLayout()

        self.interval_box = QLineEdit()
        self.key_box = QLineEdit()

        self.box_group.setExclusive(False)
        self.setWindowTitle('Sempy Configuration')
        self.setWindowIcon(QIcon('res/semaphore.png'))
        row = 0
        self.settings.beginGroup("Repositories")
        for key in self.settings.allKeys():
            self.info[key] = self.settings.value(key)

        self.main_layout.addWidget(QLabel("<b>Enable/disable repositories below:</b>"))

        for key, val in self.info.items():
            checkbox = QCheckBox(key)
            self.box_layout.addWidget(checkbox, row, 0)
            self.box_group.addButton(checkbox)
            label = QLabel()
            # icon = QIcon("res/" + val['result'] + ".svg")
            icon = QIcon("res/passed.svg")
            label.setPixmap(icon.pixmap(8))
            self.box_layout.addWidget(label, row, 1)
            row += 1

        # Needed to stop Pycharm complaining
        # noinspection PyUnresolvedReferences
        self.save_button.clicked.connect(self.save)
        # noinspection PyUnresolvedReferences
        self.reload_button.clicked.connect(self.reload)
        self.btn_layout.addWidget(self.save_button)
        self.btn_layout.addWidget(self.reload_button)

        self.main_layout.addItem(self.box_layout)
        self.main_layout.addItem(self.btn_layout)
        self.setLayout(self.main_layout)

    def save(self):
        print("save")

    def reload(self):
        print("reload")

    def closeEvent(self, event):
        event.ignore()
        self.hide()
