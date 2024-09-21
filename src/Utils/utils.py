import sys

class log:

    def __init__(self, loglevel=0, classname="NO CLASSNAME SPECIFIED") -> None:
        self.loglevel = loglevel
        self.className = classname

    def __call__(self, prefix, message, classname=""):
        return self.log(prefix, message, classname,)

    def log(self, prefix, message, className=""):
        if not className:
            className == self.className
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

