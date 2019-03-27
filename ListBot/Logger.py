import os
import time
import datetime


class Logger:

    log_file = None

    def __init__(self, clear_log=False):
        """Creates database log file."""
        if clear_log:
            if os.path.exists('logfile.txt'):
                os.remove('logfile.txt')
                self.log_file = open('logfile.txt', 'a+')
                self.enter_log("log file created")
            else:
                self.log_file = open('logfile.txt', 'a+')
                self.enter_log("log file created")
        else:
            if os.path.exists('logfile.txt'):
                self.log_file = open('logfile.txt', 'w')
            else:
                self.log_file = open('logfile.txt', 'a+')
                self.enter_log("log file created")

    def enter_log(self, s):
        """Creates log entry with current timestamp."""
        if self.log_file.closed:
            self.log_file = open('logfile.txt', 'a+')
        self.log_file.write(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')+": " + s + "\n")