import sys

class log:

    def __init__(self, loglevel=0) -> None:
        self.loglevel = loglevel

    def log(self, prefix, className, message):
        if self.loglevel == 0:
            return
        if prefix == "warning" or prefix == "error":
            if not self.loglevel > 0:
                return
        elif prefix == "info":
            if not self.loglevel > 1:
                return
        elif prefix == "verbose" or prefix == "debug":
            if not self.loglevel > 2:
                return
        print(f"[{prefix.upper()}] [{className.upper()}]: {message}")

