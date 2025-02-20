import wpilib

from subsystems.claw import Claw
from ultime.autoproperty import autoproperty
from ultime.command import Command


class RetractCoral(Command):
    speed_left = autoproperty(0.5)
    speed_right = autoproperty(-0.5)
    delay = autoproperty(1.0)

    def __init__(self, claw: Claw):
        super().__init__()
        self.claw = claw
        self.timer = wpilib.Timer()
        self.addRequirements(claw)

    def initialize(self):
        self.timer.restart()

    def execute(self):
        self.claw.setLeft(self.speed_left)
        self.claw.setRight(self.speed_right)

    def isFinished(self) -> bool:
        return self.timer.hasElapsed(self.delay)

    def end(self, interrupted: bool):
        self.claw.stop()
        self.claw.is_coral_retracted = True
