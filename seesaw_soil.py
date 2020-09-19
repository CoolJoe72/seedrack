import sys, signal, time, numpy
def signal_handler(signal, frame):
    print("\nprogram exiting gracefully")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

from board import SCL, SDA
import busio

from adafruit_seesaw.seesaw import Seesaw

i2c_bus = busio.I2C(SCL, SDA)

ss = Seesaw(i2c_bus, addr=0x36)
while True:
    touch=[]
    temp=[]
    while len(touch)<5:
        touch.append(int(ss.moisture_read()))
        temp.append(int(ss.get_temp()))
        time.sleep(1)
    # read moisture level through capacitive touch pad
    touch = int(numpy.mean(touch))

    # read temperature from the temperature sensor
    temp = int(numpy.mean(temp))

    print("temp: " + str(temp) + "  moisture: " + str(touch))
    time.sleep(1)

