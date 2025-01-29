import wpilib
from commands2 import Command

from subsystems.arm import Arm
from ultime.autoproperty import autoproperty


class ExtendArm(Command):
    delay = autoproperty(3.0)

    def __init__(self, arm: Arm):
        super().__init__()
        self.arm = arm
        self.timer = wpilib.Timer()
        self.timer.restart()
        self.addRequirements(arm)

    def execute(self):
        self.arm.moveDown()

    def isFinished(self) -> bool:
        return self.timer.get() >= self.delay

    def end(self, interrupted: bool):
        self.arm.stop()
