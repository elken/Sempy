import webbrowser

from PyQt4.QtGui import *
from PyQt4.QtCore import QSettings

from Request import *


class SempyWizard(QWizard):
    def __init__(self, parent=None):
        super(QWizard, self).__init__(parent)
        self.settings = QSettings(QSettings.IniFormat, QSettings.UserScope, "Sempy",  "config")
        self.info = {}
        self.token = None
        self.Intro_Page = 1
        self.Token_Page = 2
        self.Validation_Page = 3
        self.Filter_Page = 4
        self.Final_Page = 5
        self.setPage(self.Intro_Page, self.create_intro_page())
        self.setPage(self.Token_Page, self.create_token_page())
        self.setPage(self.Validation_Page, self.create_validation_page())
        self.setPage(self.Final_Page, self.create_final_page())

    @staticmethod
    def create_intro_page():
        intro_page = QWizardPage()
        intro_page.setTitle("Sempy Wizard")
        intro_page.setSubTitle("This wizard will go through some steps to setup Sempy")
        return intro_page

    def create_token_page(self):
        token_page = QWizardPage()
        token_page.setTitle("Authentication token entry")
        token_page.setSubTitle("Input your Semaphore token. If you don't yet have one, click the button below. "
                               "\nThen go to the settings tab of the project you wish to monitor and click on API.")

        token_label = QLabel("Your authentication token:")
        token_input = QLineEdit()
        token_label.setBuddy(token_input)
        token_page.registerField("tokenInput*", token_input)
        url_button = QPushButton("Get your token")
        # Needed to stop Pycharm complaining
        # noinspection PyUnresolvedReferences
        url_button.clicked.connect(lambda s: webbrowser.open("https://semaphoreci.com/"))

        layout = QGridLayout()
        layout.addWidget(token_label, 0, 0)
        layout.addWidget(token_input, 0, 1)
        layout.addWidget(url_button, 1, 0)
        token_page.setLayout(layout)
        self.button(QWizard.NextButton).clicked.connect(lambda s: self.update_token(token_input))
        return token_page

    def create_validation_page(self):
        validation_page = QWizardPage()
        validation_page.setTitle("Auth success")
        validation_page.setSubTitle("Proceed to the next screen to toggle repositories.")
        self.button(QWizard.NextButton).clicked.connect(lambda s: self.filter_create())
        return validation_page

    def create_filter_page(self):
        filter_page = QWizardPage()
        filter_page.setTitle("Choose which repositories to watch")
        filter_page.setSubTitle("Click the checkbox next to the repo you would like to watch. \n"
                                "This can be adjusted later in the configuration file.")
        layout = QGridLayout()
        row = 0
        box_group = QButtonGroup()
        for key, val in self.info.items():
            checkbox = QCheckBox(key)
            layout.addWidget(checkbox, row, 0)
            box_group.addButton(checkbox)
            label = QLabel()
            icon = QIcon("res/" + val['result'] + ".svg")
            label.setPixmap(icon.pixmap(8))
            layout.addWidget(label, row, 1)
            row += 1
        filter_page.setLayout(layout)
        self.button(QWizard.NextButton).clicked.connect(lambda s: self.get_checked(box_group))
        return filter_page

    def create_final_page(self):
        final_page = QWizardPage()
        final_page.setTitle("Wizard complete")
        final_page.setSubTitle("Daemon will start running once you click finish. \n"
                               "Config is located in: " + self.settings.fileName())
        return final_page

    def get_checked(self, box_group):
        if self.currentId() is self.Final_Page:
            for i in box_group.buttons():
                self.settings.beginGroup("Repositories")
                if i.isChecked() != 0:
                    self.settings.setValue(i.text(), "True")
                else:
                    self.settings.setValue(i.text(), "False")
                self.settings.endGroup()

    def update_token(self, token_input):
        if self.currentId() is self.Validation_Page:
            self.settings.setValue("token", str(token_input.text()))
            self.token = str(token_input.text())
            self.update_info()

    def update_info(self):
        if self.token is not None:
            self.info = json_to_dict(json.loads(get_json(self.token)))

    def filter_create(self):
        if self.currentId() is self.Validation_Page:
            self.setPage(self.Filter_Page, self.create_filter_page())
