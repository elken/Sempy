from threading import Thread, Event
import time


# from http://stackoverflow.com/questions/5849484/how-to-exit-a-multithreaded-program
class StoppableThread(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.stop_event = Event()

    def stop(self):
        if self.isAlive():
            self.stop_event.set()
            self.join()


class IntervalTimer(StoppableThread):

    def __init__(self, interval, worker_func):
        super().__init__()
        self._interval = interval
        self._worker_func = worker_func
        self.setName("RequestThread")

    def run(self):
        while not self.stop_event.is_set():
            self._worker_func()
            time.sleep(self._interval)
