import os
import time
import datetime


class TxtLogger:

    def __init__(self, path: str, clear_log: bool = False):
        assert isinstance(path, str), 'Argument str must be a file path in quotation marks.'
        assert isinstance(clear_log, bool), 'Argument str must be boolean.'
        """Creates database log file."""
        self.path = path
        if clear_log:
            if os.path.exists(path):
                os.remove(path)
                self.log_file = open(path, 'w')
                self.enter_log("log file created")
            else:
                self.log_file = open(path, 'w')
                self.enter_log("log file created")
        else:
            if os.path.exists(path):
                self.log_file = open(path, 'a')
            else:
                self.log_file = open(path, 'a')
                self.enter_log("log file created")

    def clear_logs(self):
        os.remove(self.path)
        self.log_file = open(self.path, 'w')
        self.enter_log("Log file cleared.")

    def enter_log(self, s):
        """Creates log entry with current timestamp."""
        if self.log_file.closed:
            self.log_file = open(self.path, 'a')
        self.log_file.write(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')+": " + s + "\n")
