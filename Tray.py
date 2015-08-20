# PyQt
from PyQt4.QtGui import *
from PyQt4.QtCore import QSettings

# Sempy
from Request import *
from IntervalTimer import *
from Logger import *


class Sempy(QSystemTrayIcon):
    def __init__(self, parent=None):
        self.settings = QSettings(QSettings.IniFormat, QSettings.UserScope, "Sempy",  "config")

        self.token = self.settings.value("token")
        self.enabled_repos = []
        self.update_enabled_repos()
        self.c = 0
        self.logger = Logger(self.settings)

        QSystemTrayIcon.__init__(self, QIcon("res/semaphore.png"), parent)
        self.menu = QMenu(parent)
        if self.token is not None:
            logging.debug("Starting RequestThread")
            interval = IntervalTimer(5, self.update_menu)
            interval.start()

    def update_menu(self):
        self.update_enabled_repos()
        self.c += 1
        logging.debug("Request #%d" % self.c)
        info = {}
        if self.token is not None:
            info = json_to_dict(json.loads(get_json(self.token)))
        self.menu.clear()
        for i in info.values():
            if self.enabled_repos.__contains__(str(i['owner'] + "/" + i['name'])):
                self.menu.addAction(QIcon("res/" + i['result'] + ".svg"), i['owner'] + "/" + i['name'])

        self.menu.addSeparator()
        self.menu.addAction("Exit", qApp.quit)
        self.setContextMenu(self.menu)

    def update_enabled_repos(self):
        self.settings.beginGroup("Repositories")
        for i in self.settings.allKeys():
            if self.settings.value(i) == "True":
                self.enabled_repos.append(i)