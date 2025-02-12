import wpilib
from wpiutil import SendableBuilder

from ports import PWM
from ultime.autoproperty import autoproperty
from ultime.subsystem import Subsystem


class Arm(Subsystem):
    speed = autoproperty(0.3)

    def __init__(self):
        super().__init__()
        self._motor = wpilib.VictorSP(PWM.arm_motor)

    def retract(self):
        self._motor.set(self.speed)

    def extend(self):
        self._motor.set(self.speed * -1)

    def stop(self):
        self._motor.stopMotor()

    def getCurrentDrawAmps(self) -> float:
        return 0.0

    def initSendable(self, builder: SendableBuilder) -> None:
        super().initSendable(builder)

        def noop(_):
            pass

        builder.addFloatProperty("motor_input", self._motor.get, noop)
        builder.addStringProperty("state", self.state.name, noop)
        builder.addStringProperty("state_movement", self.movement_state.name, noop)
