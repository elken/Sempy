import logging

# PyQt
from PyQt4.QtGui import *
from PyQt4.QtCore import *

# Sempy
from Request import *
from IntervalTimer import *
from Logger import *


class Sempy(QSystemTrayIcon):
    def __init__(self, settings, parent=None):
        self._settings = settings
        self.token = self._settings.value("token")
        self.c = 0
        self.logger = Logger(self._settings)

        QSystemTrayIcon.__init__(self, QIcon("res/semaphore.png"), parent)
        self.menu = QMenu(parent)
        if self.token is not None or self.token is not "None":
            logging.debug("Starting RequestThread")
            interval = IntervalTimer(5, self.update_menu)
            interval.start()

    def update_menu(self):
        self.c += 1
        logging.debug("Request #%d" % self.c)
        info = json_to_dict(json.loads(get_json(self.token)))
        self.menu.clear()
        for i in info.values():
            self.menu.addAction(QIcon("res/" + i['result'] + ".svg"), i['owner'] + "/" + i['name'])

        self.menu.addSeparator()
        self.menu.addAction("Exit", qApp.quit)
        self.setContextMenu(self.menu)
