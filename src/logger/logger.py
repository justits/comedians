import os
import logging

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIRECTORY = 'logs'


class Logger:
    def __init__(self, logs_file_name: str):
        self.logs_file_name = logs_file_name
        self.logger = self._setup_logger()

    def _setup_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        log_path = os.path.join(BASE_DIR, LOGS_DIRECTORY)
        if not os.path.exists(log_path):
            os.makedirs(log_path)

        file_handler = logging.FileHandler(os.path.join(log_path, self.logs_file_name))
        file_handler.setLevel(logging.ERROR)
        file_handler.setFormatter(log_format)

        logger.addHandler(file_handler)

        return logger

    def log_error(self, message):
        self.logger.error(message)
