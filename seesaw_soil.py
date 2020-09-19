import sys, signal, time
import statistics as s
from datetime import datetime, timezone
dt, tz = datetime, timezone
def signal_handler(signal, frame):
    print("\nprogram exiting gracefully")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

from board import SCL, SDA
import busio

from adafruit_seesaw.seesaw import Seesaw

i2c_bus = busio.I2C(SCL, SDA)
mmin, mmax, n = 200, 2000, 10
twet = ttemp = 0
atemp = []
btemp = []
ss = Seesaw(i2c_bus, addr=0x36)
for i in range(n): atemp.append(ss.get_temp())
print(atemp)
T = 2
while T:
    now = dt.now(tz.utc)
    wet = int(((ss.moisture_read() - mmin)*100)/(mmax-mmin))
    for x in range(n):
        atemp.append(ss.get_temp())
        print("new temp: {:.2f}".format(atemp[-1]))
        tmean = s.mean(atemp)
        print(tmean)
        btemp.append(float("{:.1f}".format(tmean)))
        print("btemp list: {}".format(btemp))
        atemp.pop(0)
        if len(btemp)>n: btemp.pop(0)
    temp = s.mode(btemp)
    print("Mode Temp: {}".format(temp))
    if temp != ttemp:
        print("{},{:.1f},{}".format(now,temp,wet))
        ttemp, twet = temp, wet
    time.sleep(1)
    T -= 1

