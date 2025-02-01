import wpilib
from commands2 import Command

from subsystems.arm import Arm
from ultime.autoproperty import autoproperty


class RetractArm(Command):

    def __init__(self, arm: Arm):
        super().__init__()
        self.arm = arm
        self.timer = wpilib.Timer()
        self.addRequirements(arm)

    def initialize(self):
        self.timer.restart()

    def execute(self):
        self.arm.retract()

    def isFinished(self) -> bool:
        return self.timer.hasElapsed(arm_properties.delay)

    def end(self, interrupted: bool):
        self.arm.stop()


class _ClassProperties:
    # Arm Properties #
    delay = autoproperty(1.0)


arm_properties = _ClassProperties()
