from PyQt4.QtCore import SIGNAL, QThread
import time
import logging


class Worker(QThread):
    def __init__(self, interval):
        QThread.__init__(self)
        self.interval = interval
        self.setObjectName("RequestThread")
        self.signal = SIGNAL("signal")

    def run(self):
        time.sleep(self.interval)
        logging.debug("Job done")
        self.emit(self.signal, "Job done")
