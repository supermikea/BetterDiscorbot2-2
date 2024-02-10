import os
import sys

command = "sleep 5 && python3 \"/home/ubuntu/discor_bot/BetterDiscorbot2-2/src/main.py\" &"

# fork the process
pid = os.fork()

if pid == 0:
    # independent process
    os.setsid()
    os.system(command)
    sys.exit(0)
else:
    sys.exit(0)