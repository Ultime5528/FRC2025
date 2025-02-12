from wpilib import VictorSP
from wpiutil import SendableBuilder

import ports
from ultime.subsystem import Subsystem
from ultime.switch import Switch


class Claw(Subsystem):
    def __init__(self):
        super().__init__()
        self._motor_right = VictorSP(ports.PWM.claw_motor_right)
        self._motor_left = VictorSP(ports.PWM.claw_motor_left)
        self._sensor = Switch(Switch.Type.NormallyOpen, ports.DIO.claw_photocell)

    def stop(self):
        self._motor_right.stopMotor()
        self._motor_left.stopMotor()

    def setRight(self, speed: float):
        self._motor_right.set(speed)

    def setLeft(self, speed: float):
        self._motor_left.set(speed)

    def hasCoralInLoader(self):
        return self._sensor.isPressed()

    def initSendable(self, builder: SendableBuilder) -> None:
        super().initSendable(builder)
        def noop(_):
            pass

        builder.addFloatProperty("motor_left", self._motor_left.get, noop)
        builder.addFloatProperty("motor_right", self._motor_right.get, noop)
        builder.addBooleanProperty("has_coral", self.hasCoralInLoader, noop)
