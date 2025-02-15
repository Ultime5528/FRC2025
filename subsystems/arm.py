from enum import Enum, auto

import wpilib

from ports import PWM
from ultime.autoproperty import autoproperty
from ultime.subsystem import Subsystem


class Arm(Subsystem):
    class State(Enum):
        Unknown = auto()
        Moving = auto()
        Extended = auto()
        Retracted = auto()

    class MovementState(Enum):
        DoNotMove = auto()
        FreeToMove = auto()
        Unknown = auto()

    speed = autoproperty(0.3)

    def __init__(self):
        super().__init__()
        self._motor = wpilib.VictorSP(PWM.arm_motor)
        self.state = Arm.State.Unknown
        self.movement_state = Arm.MovementState.Unknown

    def extend(self):
        if self.movement_state == Arm.MovementState.DoNotMove:
            self.stop()
        else:
            self.state = Arm.State.Moving
            self._motor.set(self.speed)

    def retract(self):
        if self.movement_state == Arm.MovementState.DoNotMove:
            self.stop()
        else:
            self.state = Arm.State.Moving
            self._motor.set(-self.speed)

    def stop(self):
        self._motor.stopMotor()

    def getCurrentDrawAmps(self) -> float:
        return 0.0
