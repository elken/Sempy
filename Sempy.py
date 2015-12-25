# Sempy
from Logger import *
from Request import *
from Window import *
from Worker import *

# Python STL
import sys
from queue import Queue
from os.path import dirname
from os.path import join
from os.path import realpath

# Plyer
from plyer import notification
from plyer.utils import platform


class Sempy(QSystemTrayIcon):
    message_queue = Queue()

    def __init__(self, parent=None):
        """
        ctor for the main tray widget. Initialises all the values properly and configures initial state.
        :param parent: Parent to create from
        :return: Sempy object
        """
        self.config = SempyConfig()
        self.settings = QSettings(QSettings.IniFormat, QSettings.UserScope, "Sempy",  "config")
        QSystemTrayIcon.__init__(self, QIcon("res/semaphore.png"), parent)

        if os.path.exists(self.settings.fileName()) and self.settings.value("token"):
            self.current_info = {}
            self.last_info = {}
            self.enabled_repos = []
            self.token = str(self.settings.value("token"))
            self.interval = int(self.settings.value("interval"))
            self.logger = Logger(os.path.dirname(self.settings.fileName()))
            self.req_counter = 0

            self.update_enabled_repos()

            self.menu = self.create_menu(parent)
            self.setContextMenu(self.menu)

            logging.debug("Starting RequestThread")
            self.req_thread = Worker(interval=self.interval, function=self.update_enabled_repos)
            self.req_thread.done_signal.connect(self.update_menu)
            self.req_thread.start()

    def update_menu(self):
        """
        Update the context menu upon a thread job concluding
        :return: Nothing, just modifies global state
        """
        for index, val in enumerate(self.menu.actions()):
            if not val.isSeparator() and val.text() != "Exit" and val.text() != "Config":
                last_item = self.last_info.popitem()
                val.setText(last_item[0])
                val.setIcon(QIcon("res/" + last_item[1]['result'] + ".svg"))

    def create_menu(self, parent=None):
        """
        Create the initial context menu
        :param parent: Parent widget
        :return: A constructed menu
        """
        menu = QMenu(parent)
        for i in self.current_info.values():
            if self.enabled_repos.__contains__(str(i['owner'] + "/" + i['name'])):
                if i['result'] == 'stopped':
                    file_str = "res/failed.svg"
                else:
                    file_str = "res/" + i['result'] + ".svg"
                menu.addAction(QIcon(file_str), i['owner'] + "/" + i['name'])

        menu.addSeparator()
        config_action = menu.addAction("Config")
        config_action.triggered.connect(self.config.exec)
        exit_action = menu.addAction("Exit")
        exit_action.triggered.connect(self.exit)
        return menu

    def update_current_info(self):
        """
        Update the current JSON & swap current and last
        :return: The updated JSON
        """
        self.req_counter += 1
        logging.debug("Request #{}".format(self.req_counter))
        if self.token is not None:
            self.last_info = self.current_info
            return json_to_dict(json.loads(get_json(self.token)))

    def update_enabled_repos(self):
        """ Update the list of enabled repos & their status. """
        self.current_info = self.update_current_info()
        for i in self.current_info.values():
            self.message_queue.put({str(i['owner'] + "/" + i['name']): i['result']})
            self.do_notify(str(i['owner'] + "/" + i['name']))
        self.settings.beginGroup("Repositories")
        for i in self.settings.allKeys():
            if i in self.current_info:
                if self.settings.value(i).capitalize() == "True":
                    logging.debug("{} is enabled".format(i))
                    self.enabled_repos.append(i)
            else:
                logging.debug("Removing {}, not found in current_info".format(i))
                self.settings.remove(i)
        self.settings.endGroup()

    def do_notify(self, repo):
        """
        Handles notifications.
        :param repo: Repo to generate a notification from
        """
        last_status = None
        current_status = None
        for i in self.last_info.values():
            last_status = i['result']

        for i in self.current_info.values():
            current_status = i['result']

        if all(a is not None for a in [last_status, current_status]):
            if last_status != current_status:
                message = str("Build for %s %s." % (repo, current_status))
                notification_dict = {'title': "Sempy",
                                     'message': message,
                                     'app_name': "Sempy",
                                     'timeout': 3}
                if platform == "win":
                    notification_dict['app_icon'] = join(dirname(realpath(__file__)), "res/" + current_status + ".ico")
                else:
                    notification_dict['app_icon'] = join(dirname(realpath(__file__)), "res/" + current_status + ".png")
                notification.notify(**notification_dict)

    def exit(self):
        self.req_thread.quit()
        sys.exit(0)
