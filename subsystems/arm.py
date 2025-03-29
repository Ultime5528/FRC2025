from enum import Enum, auto

import wpilib
from wpiutil import SendableBuilder

import ports
from ultime.alert import AlertType
from ultime.autoproperty import autoproperty
from ultime.subsystem import Subsystem
from ultime.timethis import tt


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

    speed = autoproperty(-0.8)

    def __init__(self):
        super().__init__()
        self._motor = wpilib.VictorSP(ports.PWM.arm_motor)
        self.state = Arm.State.Unknown
        self.movement_state = Arm.MovementState.Unknown
        self.alert_motor_hi = self.createAlert(
            "Arm motor current measured too high. "
            + f"Is it connected? PWM={ports.PWM.arm_motor} PDP={ports.PDP.arm_motor}",
            AlertType.Error,
        )
        self.alert_motor_lo = self.createAlert(
            "Arm motor current measured too low. "
            + f"Is it connected? PWM={ports.PWM.arm_motor} PDP={ports.PDP.arm_motor}",
            AlertType.Error,
        )

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

    def getMotorInput(self):
        return self._motor.get()

    def initSendable(self, builder: SendableBuilder) -> None:
        super().initSendable(builder)

        def noop(_):
            pass

        builder.addFloatProperty("motor_input", tt(self.getMotorInput), noop)
        builder.addStringProperty("state", tt(lambda: self.state.name), noop)
        builder.addStringProperty(
            "state_movement", tt(lambda: self.movement_state.name), noop
        )
