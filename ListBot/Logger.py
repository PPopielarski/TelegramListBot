import os
import time
import datetime
from ListBot import Config


class Logger:

    def __init__(self, clear_log=False):
        """Creates database log file."""
        if clear_log:
            if os.path.exists(Config.log_path):
                os.remove(Config.log_path)
                self.log_file = open(Config.log_path, 'w')
                self.enter_log("log file created")
            else:
                self.log_file = open(Config.log_path, 'w')
                self.enter_log("log file created")
        else:
            if os.path.exists(Config.log_path):
                self.log_file = open(Config.log_path, 'a')
            else:
                self.log_file = open(Config.log_path, 'a')
                self.enter_log("log file created")

    def enter_log(self, s):
        """Creates log entry with current timestamp."""
        if self.log_file.closed:
            self.log_file = open(Config.log_path, 'a')
        self.log_file.write(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')+": " + s + "\n")
