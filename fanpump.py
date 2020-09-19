#!/usr/bin/env python

# Import requited modules
import time
from gpiozero import output_devices
#import RPi.GPIO as io
#io.setmode(io.BCM)


class FanPump(SourceMixin, CompositeDevice):
    """
    Extends :class:`CompositeDevice` and represents a generic motor
    connected to a bi-directional motor driver circuit (i.e. an `H-bridge`_).

    Attach an `H-bridge`_ motor controller to your Pi; connect a power source
    (e.g. a battery pack or the 5V pin) to the controller; connect the outputs
    of the controller board to the two terminals of the motor; connect the
    inputs of the controller board to two GPIO pins.

    .. _H-bridge: https://en.wikipedia.org/wiki/H_bridge

    The following code will make the motor turn "forwards"::

        from gpiozero import Motor

        motor = Motor(17, 18)
        motor.forward()

    :type forward: int or str
    :param forward:
        The GPIO pin that the forward input of the motor driver chip is
        connected to. See :ref:`pin-numbering` for valid pin numbers. If this
        is :data:`None` a :exc:`GPIODeviceError` will be raised.

    :type backward: int or str
    :param backward:
        The GPIO pin that the backward input of the motor driver chip is
        connected to. See :ref:`pin-numbering` for valid pin numbers. If this
        is :data:`None` a :exc:`GPIODeviceError` will be raised.

    :type enable: int or str or None
    :param enable:
        The GPIO pin that enables the motor. Required for *some* motor
        controller boards. See :ref:`pin-numbering` for valid pin numbers.

    :param bool pwm:
        If :data:`True` (the default), construct :class:`PWMOutputDevice`
        instances for the motor controller pins, allowing both direction and
        variable speed control. If :data:`False`, construct
        :class:`DigitalOutputDevice` instances, allowing only direction
        control.

    :type pin_factory: Factory or None
    :param pin_factory:
        See :doc:`api_pins` for more information (this is an advanced feature
        which most users can ignore).
    """
    def __init__(self, afan=None, bfan=None, pump=None, enable=None, pwm=True,
                 pin_factory=None):
        if not all(p is not None for p in [afan, bfan, pump]):
            raise GPIOPinMissing(
                'afan, bfan, and pump pins must be provided'
            )
        PinClass = PWMOutputDevice if pwm else DigitalOutputDevice
        devices = OrderedDict((
            ('afan_device', PinClass(afan)),
            ('bfan_device', PinClass(bfan)),
        ))
        if enable is not None:
            devices['enable_device'] = DigitalOutputDevice(enable,
                                                           initial_value=True)
        super(FanPump, self).__init__(_order=devices.keys(), **devices)

    @property
    def value(self):
        """
        Represents the speed of the motor as a floating point value between -1
        (full speed backward) and 1 (full speed forward), with 0 representing
        stopped.
        """
        return self.forward_device.value - self.backward_device.value

    @value.setter
    def value(self, value):
        if not -1 <= value <= 1:
            raise OutputDeviceBadValue("Motor value must be between -1 and 1")
        if value > 0:
            try:
                self.forward(value)
            except ValueError as e:
                raise OutputDeviceBadValue(e)
        elif value < 0:
            try:
               self.backward(-value)
            except ValueError as e:
                raise OutputDeviceBadValue(e)
        else:
            self.stop()

    @property
    def is_active(self):
        """
        Returns :data:`True` if the motor is currently running and
        :data:`False` otherwise.
        """
        return self.value != 0

    def forward(self, speed=1):
        """
        Drive the motor forwards.

        :param float speed:
            The speed at which the motor should turn. Can be any value between
            0 (stopped) and the default 1 (maximum speed) if *pwm* was
            :data:`True` when the class was constructed (and only 0 or 1 if
            not).
        """
        if not 0 <= speed <= 1:
            raise ValueError('forward speed must be between 0 and 1')
        if isinstance(self.forward_device, DigitalOutputDevice):
            if speed not in (0, 1):
                raise ValueError(
                    'forward speed must be 0 or 1 with non-PWM Motors')
        self.backward_device.off()
        self.forward_device.value = speed


    def backward(self, speed=1):
        """
        Drive the motor backwards.

        :param float speed:
            The speed at which the motor should turn. Can be any value between
            0 (stopped) and the default 1 (maximum speed) if *pwm* was
            :data:`True` when the class was constructed (and only 0 or 1 if
            not).
        """
        if not 0 <= speed <= 1:
            raise ValueError('backward speed must be between 0 and 1')
        if isinstance(self.backward_device, DigitalOutputDevice):
            if speed not in (0, 1):
                raise ValueError(
                    'backward speed must be 0 or 1 with non-PWM Motors')
        self.forward_device.off()
        self.backward_device.value = speed


    def reverse(self):
        """
        Reverse the current direction of the motor. If the motor is currently
        idle this does nothing. Otherwise, the motor's direction will be
        reversed at the current speed.
        """
        self.value = -self.value


    def stop(self):
        """
        Stop the motor.
        """
        self.forward_device.off()
        self.backward_device.off()



pout=[5,6,16,19,20,21,26,12,13]
pname=['stby','pump2','fan1a','fan2a','fan1b','pump1','fan2b','fan1pwm','fan2pwm']
pin=[18,23,24,25]
psence['stop1','dry1','stop2','dry2']

for o in po:
    io.setup(o, io.OUT)
for i in pi:
    io.setup(i, io.IN)
for p in pwm:
    io.PWM(p, 100)

