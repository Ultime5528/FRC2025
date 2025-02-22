import wpilib
from commands2 import Command

from subsystems.claw import Claw
from ultime.autoproperty import autoproperty


class LoadCoral(Command):

    def __init__(self, claw: Claw):
        super().__init__()
        self.claw = claw
        self.addRequirements(claw)
        self.timer = wpilib.Timer()
        self.speed_left = load_coral_properties.speed_left
        self.speed_right = load_coral_properties.speed_right

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

class _ClassProperties:
    # Claw Properties #
    delay = autoproperty(0.0, subtable=LoadCoral.__name__)
    speed_left = autoproperty(-0.6, subtable=LoadCoral.__name__)
    speed_right = autoproperty(0.6, subtable=LoadCoral.__name__)


load_coral_properties = _ClassProperties()
