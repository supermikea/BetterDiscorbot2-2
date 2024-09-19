import sys
from enum import Enum

class log(Enum):
    NONE = -1
    VERBOSE = 0
    DEBUG = 1
    INFO = 2
    
    def __init__(self, loglevel):
        if not loglevel == isinstance(loglevel, log):
            raise Exception("loglevel is not a enum from class log!")
            sys.exit(1)
        self.loglevel = loglevel

    def Log(self, loglevel, message):
        # TODO
        print(f"[{self.loglevel.name}]: {message}")

