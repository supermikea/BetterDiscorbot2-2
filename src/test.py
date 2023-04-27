import time
import datetime

begin_time = time.time()

time.sleep(1)

end_time = time.time()

duration = end_time - begin_time

# print duration
print(time.strftime("%H:%M:%S", time.gmtime(duration)))