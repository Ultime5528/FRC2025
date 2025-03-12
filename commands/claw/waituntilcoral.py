import wpilib
from commands2 import Command

from subsystems.claw import Claw
from ultime.autoproperty import autoproperty
from ultime.command import ignore_requirements


@ignore_requirements(["claw"])
class WaitUntilCoral(Command):

    def __init__(self, claw: Claw):
        super().__init__()
        self.claw = claw
        self.timer = wpilib.Timer()

    def initialize(self):
        self.timer.stop()
        self.timer.reset()
        self.timer.start()

    def isFinished(self) -> bool:
        return self.claw.seesObject() or self.timer.get() >= _properties.timeout


class _ClassProperties:
    timeout = autoproperty(3, subtable=WaitUntilCoral.__name__)


_properties = _ClassProperties()
