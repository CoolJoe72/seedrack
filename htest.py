import sys, signal
import threading
from time import sleep, time
from gpiozero import Motor, PWMOutputDevice, OutputDevice, Button
print("starting…")

def signal_handler(signal, frame):
    print("\nprogram exiting gracefully")
    stopFans()
    pump1.off()
    sys.exit(0)
stime = None
ftimer = 30
stby = OutputDevice(5,active_high=False)
pump1,pump2 = OutputDevice(21),OutputDevice(6)
pwm1, pwm2 = PWMOutputDevice(12),PWMOutputDevice(13)
fans1,fans2 = Motor(16,20),Motor(19,26)
waterfull = Button(18)
wbase = Button(23)
print("pins set…")

def runPump():
    print("Starting Pump")
    pump1.on()

def swapFans():
    while True:
        fans1.reverse()
        sleep(ftimer)

def startFans():
    print("turning things on…")
    stby.off()
    fans1.forward()
    pwm1.value=0.01
    print("things on…")

def stopFans():
    print("turning things off…")
    fans1.stop()
    stby.on()
    pwm1.off()
    print("…all done")

def startTimer():
    stime = time()

startFans()

b = threading.Thread(name='swapFans', target=swapFans)
b.daemon = True
b.start()
t = threading.Timer(30, runPump)
t.daemon = True
waterfull.when_pressed = pump1.off
wbase.when_released = startTimer
while True:
    signal.signal(signal.SIGINT, signal_handler)
    if stime > time
