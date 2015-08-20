from PyQt4.QtGui import *
from PyQt4.QtCore import QSettings
import webbrowser


class SempyWizard(QWizard):
    def __init__(self, parent=None):
        super(QWizard, self).__init__(parent)
        self.settings = QSettings(QSettings.IniFormat, QSettings.UserScope, "Sempy",  "config")
        self.addPage(self.create_intro_page())
        self.addPage(self.create_token_page())
        self.addPage(self.create_final_page())

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
        url_button.clicked.connect(lambda s: webbrowser.open("https://semaphoreci.com/"))

        layout = QGridLayout()
        layout.addWidget(token_label, 0, 0)
        layout.addWidget(token_input, 0, 1)
        layout.addWidget(url_button, 1, 0)
        token_page.setLayout(layout)
        self.button(QWizard.NextButton).clicked.connect(lambda s: self.settings.setValue("token",
                                                                                         str(token_input.text())))
        return token_page

    def create_final_page(self):
        final_page = QWizardPage()
        final_page.setTitle("Wizard complete")
        final_page.setSubTitle("Daemon will start running once you click finish. \n"
                               "Config is located in: " + self.settings.fileName())
        return final_page
