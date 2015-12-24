import webbrowser

from PyQt4.QtGui import *
from PyQt4.QtCore import QSettings

from Request import *


class SempyWizard(QWizard):
    info = {}
    token = None
    intro_page = 1
    token_page = 2
    validation_page = 3
    filter_page = 4
    final_page = 5
    settings = QSettings(QSettings.IniFormat, QSettings.UserScope, "Sempy", "config")

    def __init__(self):
        super(SempyWizard, self).__init__()
        self.setPage(self.intro_page, IntroPage())
        self.setPage(self.token_page, TokenPage())
        self.setPage(self.validation_page, ValidationPage())
        self.setPage(self.filter_page, FilterPage())
        self.setPage(self.final_page, FinalPage())


class IntroPage(QWizardPage):
    def __init__(self, parent=None):
        super(IntroPage, self).__init__(parent)
        self.setTitle("Sempy Wizard")
        self.setSubTitle("This wizard will go through some steps to setup Sempy")


class TokenPage(QWizardPage):
    def __init__(self, parent=None):
        super(TokenPage, self).__init__(parent)

        self.setTitle("Authentication token entry")
        self.setSubTitle("Input your Semaphore token. If you don't yet have one, click the button below. "
                         "\nThen go to the settings tab of the project you wish to monitor and click on API.")

        token_label = QLabel("Your authentication token:")
        self.token_input = QLineEdit()
        token_label.setBuddy(self.token_input)
        self.registerField("tokenInput*", self.token_input)
        url_button = QPushButton("Get your token")
        # Needed to stop Pycharm complaining
        # noinspection PyUnresolvedReferences
        url_button.clicked.connect(lambda s: webbrowser.open("https://semaphoreci.com/"))

        layout = QGridLayout()
        layout.addWidget(token_label, 0, 0)
        layout.addWidget(self.token_input, 0, 1)
        layout.addWidget(url_button, 1, 0)
        self.setLayout(layout)


class ValidationPage(QWizardPage):
    def __init__(self, parent=None):
        super(ValidationPage, self).__init__(parent)

        self.setTitle("Auth success")
        self.setSubTitle("Proceed to the next screen to toggle repositories.")

    def initializePage(self):
        token = self.wizard().page(SempyWizard.token_page).token_input.text()
        if token is not None:
            try:
                SempyWizard.info = json_to_dict(json.loads(get_json(token)))
            except TypeError:
                ret = QMessageBox.critical(QMessageBox(), "Auth failed", "Click ok to restart the wizard and try again")
                if ret:
                    self.wizard().back()
            else:
                SempyWizard.settings.setValue("token", token)


class FilterPage(QWizardPage):
    box_group = QButtonGroup()

    def __init__(self, parent=None):
        super(FilterPage, self).__init__(parent)
        self.setTitle("Choose which repositories to watch")
        self.setSubTitle("Click the checkbox next to the repo you would like to watch. \n"
                         "This can be adjusted later in the configuration file.")

    def initializePage(self):
        self.box_group.setExclusive(False)
        layout = QGridLayout()
        row = 0

        for key, val in SempyWizard.info.items():
            checkbox = QCheckBox(key)
            layout.addWidget(checkbox, row, 0)
            self.box_group.addButton(checkbox)
            label = QLabel()
            icon = QIcon("res/" + val['result'] + ".svg")
            label.setPixmap(icon.pixmap(8))
            layout.addWidget(label, row, 1)
            row += 1
        self.setLayout(layout)


class FinalPage(QWizardPage):
    def __init__(self, parent=None):
        super(FinalPage, self).__init__(parent)
        self.setTitle("Wizard complete")
        self.setSubTitle("Daemon will start running once you click finish. \n"
                         "Config is located in: " + SempyWizard.settings.fileName())

    def initializePage(self):
        SempyWizard.settings.setValue("interval", 5)
        for i in FilterPage.box_group.buttons():
            SempyWizard.settings.beginGroup("Repositories")
            if i.isChecked() is True:
                SempyWizard.settings.setValue(i.text(), "True")
            else:
                SempyWizard.settings.setValue(i.text(), "False")
            SempyWizard.settings.endGroup()
