import sys, signal, time
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
mmin, mmax, tv = 200, 2000, 0.7
twet = ttemp = 0
ss = Seesaw(i2c_bus, addr=0x36)
while True:
    now = dt.now(tz.utc)
    wet = int(((ss.moisture_read() - mmin)*100)/(mmax-mmin))
    temp = float("{:.1f}".format(ss.get_temp()))
    #temp = int((ss.get_temp() * 9/5) + 32)
    if twet > wet+1 or twet < wet-1 or ttemp > temp+tv or ttemp < temp-tv:
        print("{},{},{}".format(now,temp,wet))
        ttemp, twet = temp, wet
    time.sleep(1)

