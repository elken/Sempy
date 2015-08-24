# PyQt
from PyQt4.QtGui import *
from PyQt4.QtCore import QSettings

# Sempy
from Request import *
from StoppableThread import *
from Logger import *

# Python STL
import sys
from queue import Queue
import time
from os.path import dirname
from os.path import join
from os.path import realpath

# Plyer
from plyer import notification
from plyer.utils import platform


class Sempy(QSystemTrayIcon):
    message_queue = Queue()

    def __init__(self, parent=None):
        self.settings = QSettings(QSettings.IniFormat, QSettings.UserScope, "Sempy",  "config")
        QSystemTrayIcon.__init__(self, QIcon("res/semaphore.png"), parent)

        # kwargs = {'title': "Sempy",
        #           'message': "body",
        #           'app_name': "Sempy",
        #           'app_icon':  join(dirname(realpath(__file__)), "res/semaphore.ico")}
        #
        # notification.notify(**kwargs)
        if os.path.exists(self.settings.fileName()) and self.settings.value("token"):
            self.current_info = {}
            self.last_info = {}
            self.enabled_repos = []
            self.token = str(self.settings.value("token"))
            self.interval = int(self.settings.value("interval"))
            self.update_enabled_repos()
            self.req_counter = 0
            self.logger = Logger(self.settings)

            self.menu = QMenu(parent)
            logging.debug("Starting RequestThread")
            self.create_menu()
            time.sleep(15)
            self.update_menu()
            c = 0
            while not self.message_queue.empty():
                print("Item #%d: %s" % (c, self.message_queue.get()))
                c += 1
            sys.exit(0)
            # self.req_thread = StoppableThread(self.interval, self.update_menu)
            # self.req_thread.start()

    def update_menu(self):
        self.req_counter += 1
        logging.debug("Request #%d" % self.req_counter)
        self.update_enabled_repos()
        for i in self.menu.actions():
            if not i.isSeparator() and i.text() != "Exit":
                i.setText("Changed by update_menu")
                i.setIcon(QIcon("res/failed.svg"))

    def create_menu(self):
        for i in self.current_info.values():
            if self.enabled_repos.__contains__(str(i['owner'] + "/" + i['name'])):
                if i['result'] == 'stopped':
                    file_str = "res/failed.svg"
                else:
                    file_str = "res/" + i['result'] + ".svg"
                self.menu.addAction(QIcon(file_str), i['owner'] + "/" + i['name'])

        self.menu.addSeparator()
        exit_action = self.menu.addAction("Exit")
        exit_action.triggered.connect(self.exit)
        self.setContextMenu(self.menu)

    def update_enabled_repos(self):
        if self.token is not None:
            self.last_info = self.current_info
            self.current_info = json_to_dict(json.loads(get_json(self.token)))
            for i in self.current_info.values():
                self.message_queue.put({str(i['owner'] + "/" + i['name']): i['result']})
                self.do_notify(str(i['owner'] + "/" + i['name']))
        self.settings.beginGroup("Repositories")
        for i in self.settings.allKeys():
            if i in self.current_info:
                if self.settings.value(i).capitalize() == "True":
                    self.enabled_repos.append(i)
            else:
                self.settings.remove(i)

    def do_notify(self, repo):
        last_status = None
        current_status = None
        for i in self.last_info.values():
            last_status = i['result']

        for i in self.current_info.values():
            current_status = i['result']

        if last_status != current_status:
            # if current_status == 'pending':
            message = str("Build for %s is %s." % (repo, current_status))
            notification_dict = {'title': "Sempy",
                                 'message': message,
                                 'app_name': "Sempy"}
            if platform == "win":
                notification_dict['app_icon'] = join(dirname(realpath(__file__)), "res/semaphore.ico")
            else:
                notification_dict['app_icon'] = join(dirname(realpath(__file__)), "res/semaphore.png")
            notification.notify(**notification_dict)

    def exit(self):
        # self.req_thread.stop()
        sys.exit(0)
