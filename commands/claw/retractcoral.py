import wpilib

from subsystems.claw import Claw
from ultime.autoproperty import autoproperty, FloatProperty, asCallable
from ultime.command import Command


class RetractCoral(Command):
    @classmethod
    def up(cls, claw: Claw):
        cmd = cls(
            claw,
            lambda: retract_properties.speed_left,
            lambda: retract_properties.speed_right,
        )
        cmd.setName(cmd.getName() + ".up")
        return cmd

    @classmethod
    def down(cls, claw: Claw):
        cmd = cls(
            claw,
            lambda: -retract_properties.speed_left,
            lambda: -retract_properties.speed_right,
        )
        cmd.setName(cmd.getName() + ".down")
        return cmd

    def __init__(
        self, claw: Claw, speed_left: FloatProperty, speed_right: FloatProperty
    ):
        super().__init__()
        self.claw = claw
        self.timer = wpilib.Timer()
        self.addRequirements(claw)

        self.get_speed_left = asCallable(speed_left)
        self.get_speed_right = asCallable(speed_right)

    def initialize(self):
        self.timer.restart()

    def execute(self):
        self.claw.setLeft(self.get_speed_left())
        self.claw.setRight(self.get_speed_right())

    def isFinished(self) -> bool:
        return self.timer.hasElapsed(retract_properties.delay)

    def end(self, interrupted: bool):
        self.claw.stop()
        self.claw.is_coral_retracted = not self.claw.is_coral_retracted


class _ClassProperties:
    speed_left = autoproperty(0.5, subtable=RetractCoral.__name__)
    speed_right = autoproperty(-0.5, subtable=RetractCoral.__name__)
    delay = autoproperty(0.25, subtable=RetractCoral.__name__)


retract_properties = _ClassProperties()
