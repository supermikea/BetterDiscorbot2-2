import os
import sys

pwd = os.path.dirname(os.path.realpath(__file__))
command = f"sleep 5 && python3 \"{pwd}/main.py\" &"

# fork the process
pid = os.fork()

if pid == 0:
    # independent process
    os.setsid()
    os.system(command)
    print("DYING")
    sys.exit(0)
else:
    print("DYING 2")
    sys.exit(0)