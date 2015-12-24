import logging
import time
from threading import Event

from PyQt4.QtCore import QThread, pyqtSignal


class Worker(QThread):
    done_signal = pyqtSignal(object)

    def __init__(self, interval=5, function=lambda s: print("Hello")):
        """
        Define a stoppable worker, which emits a signal after each succesful job
        :param interval: How often to wait between executions (default 5)
        :param function: The function to execute (default lambda to print "Hello")
        :return: A Worker thread
        """
        QThread.__init__(self)
        self.interval = interval
        self.function = function
        self.finished = Event()

    def stop(self):
        """ Stop execution and join the thread """
        self.finished.set()
        self.join()

    def run(self):
        """ Run `function()` every `interval` seconds, and emit a signal after each is completed. """
        while not self.finished.isSet():
            self.function()
            logging.debug("Job done")
            self.done_signal.emit("Job done")
            time.sleep(self.interval)
