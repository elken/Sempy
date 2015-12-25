import logging
import time
from threading import Event

from PyQt4.QtCore import QThread, pyqtSignal


class Worker(QThread):
    done_signal = pyqtSignal(object)

    def __init__(self, interval=5, function=lambda s: print("Hello"), args=None):
        """
        Define a stoppable worker, which emits a signal after each succesful job
        :param interval: How often to wait between executions (default 5)
        :param function: The function to execute (default lambda to print "Hello")
        :param args: Arguments to the function (default None)
        :return: A Worker thread
        """
        QThread.__init__(self)
        self.interval = interval
        self.function = function
        if args:
            self.args = args
        self.finished = Event()

    def stop(self):
        """ Stop execution and join the thread """
        self.finished.set()
        self.join()

    def run(self):
        """ Run `function()` every `interval` seconds, and emit a signal after each is completed. """
        while not self.finished.isSet():
            time.sleep(self.interval)
            try:
                logging.debug("Running {} with {}".format(self.function.__name__, self.args))
                result = self.function(self.args)
            except AttributeError:
                logging.debug("Running {} without args".format(self.function.__name__))
                result = self.function()
            self.done_signal.emit("Job done, got {}".format(result))
