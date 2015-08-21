from threading import Thread, Event
import logging


class StoppableThread(Thread):
    def __init__(self, interval, function):
        Thread.__init__(self, name="RequestThread")
        self.interval = interval
        self.function = function
        self.finished = Event()

    def stop(self):
        self.finished.set()
        logging.debug("Stopping thread")
        self.join()

    def run(self):
        while not self.finished.isSet():
            self.function()
            self.finished.wait(self.interval)
