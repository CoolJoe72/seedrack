import sys, signal, time, busio
import statistics as s
import w1temp as wt
from datetime import datetime, timezone
from board import SCL, SDA
from adafruit_seesaw.seesaw import Seesaw
dt, tz = datetime, timezone
i2c_bus = busio.I2C(SCL, SDA)
mmin, mmax, n = 200, 2000, 5
twet, ttemp = 0, 0
atemp = []
btemp = []
awet = []
bwet = []
p = False
f = True
t = .5
ss = Seesaw(i2c_bus, addr=0x36)

def signal_handler(signal, frame):
    print("\nprogram exiting gracefully")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def cf(ctemp):
    if f: return int((ctemp * 9/5) +32)
    else: return float("{:.1f}".format(ctemp))

def pformat(raw):
    if p: return int(((raw - mmin)*100)/(mmax-mmin))
    else: return float("{:.2f}".format((raw-mmin)/(mmax-mmin)))

print("Loading averages!")
for i in range(n):
    atemp.append(ss.get_temp())
    awet.append(ss.moisture_read())
    time.sleep(.1)

while True:
    now = dt.utcnow()

    atemp.append(ss.get_temp())
    tmean = s.mean(atemp)
    tsd = s.stdev(atemp, xbar = tmean)
    #print(tsd,' | ',cf(tmean),' | ',atemp)
    atemp.pop(0)
    btemp.append(cf(tmean))
    if len(btemp)>3: btemp.pop(0)
    #print(btemp)
    if len(btemp)>1 and len(btemp) == len(set(btemp)): temp = btemp[1]
    else: temp = s.mode(btemp)
    
    awet.append(ss.moisture_read())
    wmean = s.mean(awet)
    wsd = s.stdev(awet, xbar = wmean)
    #print(wsd,' | ',pformat(wmean),' | ',awet)
    awet.pop(0)
    bwet.append(pformat(wmean))
    if len(bwet)>3: bwet.pop(0)
    #print(bwet)
    if len(bwet)>1 and len(bwet) == len(set(bwet)): wet = bwet[1]
    else: wet = s.mode(bwet)

    if temp!=ttemp or wet!=twet:
        print("{},{},{}".format(now,temp,wet))
        print("{},10-0008026a7e80,{}".format(now,wt.getftemp("10-0008026a7e80")))
        ttemp, twet = temp, wet

    if tsd>.2 or wsd>35: t=.5
    elif t<180: t += 5
    #print(t)
    time.sleep(t)

