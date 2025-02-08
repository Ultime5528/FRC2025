import wpilib
from commands2 import Command

from subsystems.arm import Arm
from ultime.autoproperty import autoproperty


class ExtendArm(Command):

    def __init__(self, arm: Arm):
        super().__init__()
        self.arm = arm
        self.timer = wpilib.Timer()
        self.addRequirements(arm)

    def initialize(self):
        self.timer.restart()

    def execute(self):
        self.arm.extend()

    def isFinished(self) -> bool:
        return self.timer.get() >= arm_properties.delay

    def end(self, interrupted: bool):
        self.arm.stop()

        if interrupted:
            self.arm.state = Arm.State.Unknown
        else:
            self.arm.state = Arm.State.Extended


class _ClassProperties:
    # Arm Properties #
    delay = autoproperty(1.0)


arm_properties = _ClassProperties()
