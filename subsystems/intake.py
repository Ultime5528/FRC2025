from enum import Enum, auto

from wpilib import VictorSP, Encoder

import ports
from ultime.autoproperty import autoproperty
from ultime.subsystem import Subsystem
from ultime.switch import Switch


class Intake(Subsystem):
    class State(Enum):
        Invalid = auto()
        Moving = auto()
        Reset = auto()
        Extended = auto()
        Retracted = auto()

    pivot_speed = autoproperty(0.5)
    grab_speed = autoproperty(0.3)
    pivot_encoder_threshold = autoproperty(50)
    grab_delay = autoproperty(3)
    pivot_height_max = autoproperty(0)

    def __init__(self):
        super().__init__()

        self.pivot_motor = VictorSP(ports.PWM.intake_motor_pivot)
        self.pivot_encoder = Encoder(ports.DIO.intake_encoder)
        self.pivot_switch = Switch(
            switch_type=Switch.Type.NormallyOpen, port=ports.DIO.intake_switch_pivot
        )

        self.grab_motor = VictorSP(ports.PWM.intake_motor_grab)
        self.grab_switch = Switch(
            Switch.Type.NormallyOpen, ports.DIO.intake_switch_grab
        )

        self._has_reset = False
        self._prev_is_in = False
        self._offset = 0.0

    def periodic(self) -> None:
        if self._prev_is_in and not self.pivot_switch.isPressed():
            self._offset = self.pivot_height_max - self.pivot_encoder.getPosition()
            self._has_reset = True
        self._prev_is_in = self.pivot_switch.isPressed()

    def retractPivot(self):
        if not self.pivot_switch.isPressed():
            self.pivot_motor.set(self.pivot_speed)

    def extendPivot(self):
        self.pivot_motor.set(-1 * self.pivot_speed)

    def stopPivot(self):
        self.pivot_motor.stopMotor()

    def setSpeedPivot(self, speed: float):
        self.pivot_motor.set(speed)

    def grab(self):
        self.grab_motor.set(self.grab_speed)

    def drop(self):
        self.grab_motor.set(-1 * self.grab_speed)

    def stopGrab(self):
        self.grab_motor.stopMotor()

    def getPos(self):
        # getPosition
        return self.pivot_encoder.get()

    def hasReset(self):
        return self._has_reset

    def isIn(self):
        return self.pivot_switch.isPressed()

    def getMotorInput(self):
        return self.pivot_motor.get()

    def getCurrentDrawAmps(self) -> float:
        pass
