# PyQt
from PyQt4.QtGui import *
from PyQt4.QtCore import QSettings

# Sempy
from Request import *
from StoppableThread import *
from Logger import *

# Python STL
import sys
from os.path import dirname
from os.path import join
from os.path import realpath

# Plyer
from plyer import notification


class Sempy(QSystemTrayIcon):
    def __init__(self, parent=None):
        self.settings = QSettings(QSettings.IniFormat, QSettings.UserScope, "Sempy",  "config")

        # kwargs = {'title': "Sempy",
        #           'message': "body",
        #           'app_name': "Sempy",
        #           'app_icon':  join(dirname(realpath(__file__)), "res/semaphore.ico")}
        #
        # notification.notify(**kwargs)
        self.info = {}
        self.token = str(self.settings.value("token"))
        self.interval = int(self.settings.value("interval"))
        self.enabled_repos = []
        self.update_enabled_repos()
        self.req_counter = 0
        self.logger = Logger(self.settings)

        QSystemTrayIcon.__init__(self, QIcon("res/semaphore.png"), parent)
        self.menu = QMenu(parent)
        logging.debug("Starting RequestThread")
        self.req_thread = StoppableThread(self.interval, self.update_menu)
        self.req_thread.start()

    def update_menu(self):
        self.update_enabled_repos()
        self.req_counter += 1
        logging.debug("Request #%d" % self.req_counter)
        if self.token is not None:
            self.info = json_to_dict(json.loads(get_json(self.token)))
        self.menu.clear()
        for i in self.info.values():
            if self.enabled_repos.__contains__(str(i['owner'] + "/" + i['name'])):
                self.menu.addAction(QIcon("res/" + i['result'] + ".svg"), i['owner'] + "/" + i['name'])

        self.menu.addSeparator()
        exit_action = self.menu.addAction("Exit")
        exit_action.triggered.connect(self.exit)
        self.setContextMenu(self.menu)

    def update_enabled_repos(self):
        if self.token is not None:
            self.info = json_to_dict(json.loads(get_json(self.token)))
        self.settings.beginGroup("Repositories")
        for i in self.settings.allKeys():
            if i in self.info:
                if bool(self.settings.value(i).capitalize()) is True:
                    self.enabled_repos.append(i)
            else:
                self.settings.remove(i)

    def exit(self):
        self.req_thread.stop()
        sys.exit(0)
