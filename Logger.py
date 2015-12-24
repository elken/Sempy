import logging
import os


class Logger:
    def __init__(self, path):
        """
        Basic class to just handle how logging is formatted.
        :param path: Path to save logfile
        :return: Logging object
        """
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        handler = logging.StreamHandler()
        formatter = logging.Formatter("[%(asctime)s] [%(threadName)-13s] --- %(message)s (%(filename)s:%(lineno)s)",
                                      "%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        handler = logging.FileHandler(os.path.join(path, "sempy.log"), "w")
        formatter = logging.Formatter("[%(asctime)s] [%(threadName)-13s] --- %(message)s (%(filename)s:%(lineno)s)",
                                      "%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
