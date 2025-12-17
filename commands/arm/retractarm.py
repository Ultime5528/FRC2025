import wpilib
from commands2 import Command

from subsystems.arm import Arm
from ultime.autoproperty import autoproperty


class RetractArm(Command):
    delay = autoproperty(0.5)

    def __init__(self, arm: Arm):
        super().__init__()
        self.arm = arm
        self.timer = wpilib.Timer()
        self.addRequirements(arm)
        self.has_moved = False

    def initialize(self):
        self.timer.stop()
        self.timer.reset()
        self.has_moved = False

    def execute(self):
        if self.arm.movement_state == Arm.MovementState.DoNotMove:
            self.arm.stop()
            self.timer.reset()
        else:
            self.timer.start()
            self.arm.retract()
            self.has_moved = True

    def isFinished(self) -> bool:
        return self.timer.hasElapsed(self.delay)

    def end(self, interrupted: bool):
        self.arm.stop()

        if self.has_moved:
            if interrupted:
                self.arm.state = Arm.State.Unknown
            else:
                self.arm.state = Arm.State.Retracted
