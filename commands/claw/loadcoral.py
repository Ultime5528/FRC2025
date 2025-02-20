import wpilib
from commands2 import Command

from subsystems.claw import Claw
from ultime.autoproperty import autoproperty


class LoadCoral(Command):
    delay = autoproperty(0.0)
    speed_left = autoproperty(-0.2)
    speed_right = autoproperty(0.2)

    def __init__(self, claw: Claw):
        super().__init__()
        self.claw = claw
        self.addRequirements(claw)
        self.timer = wpilib.Timer()

    def initialize(self):
        self.timer.stop()
        self.timer.reset()

    def execute(self):
        self.claw.setLeft(self.speed_left)
        self.claw.setRight(self.speed_right)

        if not self.claw.seesObject():
            self.timer.start()
        else:
            self.timer.stop()
            self.timer.reset()

    def isFinished(self) -> bool:
        return not self.claw.seesObject() and self.timer.get() >= self.delay

    def end(self, interrupted: bool):
        self.claw.stop()
        self.timer.stop()
        if not interrupted:
            self.claw.has_coral = True
