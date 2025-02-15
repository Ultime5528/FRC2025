import wpilib
from commands2 import Command

from subsystems.arm import Arm
from ultime.autoproperty import autoproperty


class RetractArm(Command):
    delay = autoproperty(1.0)

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
        return self.timer.hasElapsed(self.delay)

    def end(self, interrupted: bool):
        self.arm.stop()

        if interrupted:
            self.arm.state = Arm.State.Unknown
        else:
            self.arm.state = Arm.State.Retracted
