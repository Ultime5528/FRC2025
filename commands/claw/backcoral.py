import wpilib

from subsystems.claw import Claw
from ultime.autoproperty import autoproperty
from ultime.command import Command


class BackCoral(Command):
    speed = autoproperty(-0.5)
    delay = autoproperty(0.2)

    def __init__(
        self,
        claw: Claw,
    ):
        super().__init__()
        self.claw = claw
        self.timer = wpilib.Timer()
        self.addRequirements(claw)

    def initialize(self):
        self.timer.restart()

    def execute(self):
        self.claw.setLeft(self.speed)
        self.claw.setRight(self.speed)

    def isFinished(self) -> bool:
        return self.timer.hasElapsed(self.delay)

    def end(self, interrupted: bool):
        self.claw.stop()
        self.claw.coral_is_retracted = True
