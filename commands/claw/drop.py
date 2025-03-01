import wpilib
from commands2 import Command

from subsystems.claw import Claw
from ultime.autoproperty import autoproperty, FloatProperty, asCallable


class Drop(Command):
    @classmethod
    def atLevel1(cls, claw: Claw):
        cmd = cls(
            claw,
            lambda: drop_properties.speed_level_1_left,
            lambda: drop_properties.speed_level_1_right,
        )
        cmd.setName(cmd.getName() + ".atLevel1")
        return cmd

    @classmethod
    def atLevel2(cls, claw: Claw):
        cmd = cls(
            claw,
            lambda: drop_properties.speed_level_2_left,
            lambda: drop_properties.speed_level_2_right,
        )

        cmd.setName(cmd.getName() + ".atLevel2")
        return cmd

    @classmethod
    def atLevel3(cls, claw: Claw):
        cmd = cls(
            claw,
            lambda: drop_properties.speed_level_3_left,
            lambda: drop_properties.speed_level_3_right,
        )

        cmd.setName(cmd.getName() + ".atLevel3")
        return cmd

    @classmethod
    def atLevel4(cls, claw: Claw):
        cmd = cls(
            claw,
            lambda: drop_properties.speed_level_4_left,
            lambda: drop_properties.speed_level_4_right,
        )

        cmd.setName(cmd.getName() + ".atLevel4")
        return cmd

    def __init__(
        self,
        claw: Claw,
        speed_left: FloatProperty,
        speed_right: FloatProperty,
    ):
        super().__init__()
        self.claw = claw
        self.get_speed_left = asCallable(speed_left)
        self.get_speed_right = asCallable(speed_right)
        self.timer = wpilib.Timer()
        self.addRequirements(claw)

    def initialize(self):
        self.timer.restart()

    def execute(self):
        speed_left = self.get_speed_left()
        self.claw.setLeft(speed_left)

        speed_right = self.get_speed_right()
        self.claw.setRight(speed_right)

    def isFinished(self) -> bool:
        return self.timer.hasElapsed(drop_properties.delay)

    def end(self, interrupted: bool):
        self.claw.stop()
        self.claw.is_coral_retracted = False
        self.claw.has_coral = False


class _ClassProperties:
    # Claw Properties #
    speed_level_1_left = autoproperty(-1.0, subtable=Drop.__name__)
    speed_level_1_right = autoproperty(0.5, subtable=Drop.__name__)
    speed_level_2_left = autoproperty(-1.0, subtable=Drop.__name__)
    speed_level_2_right = autoproperty(1.0, subtable=Drop.__name__)
    speed_level_3_left = autoproperty(-1.0, subtable=Drop.__name__)
    speed_level_3_right = autoproperty(1.0, subtable=Drop.__name__)
    speed_level_4_left = autoproperty(-1.0, subtable=Drop.__name__)
    speed_level_4_right = autoproperty(1.0, subtable=Drop.__name__)
    delay = autoproperty(1.0, subtable=Drop.__name__)


drop_properties = _ClassProperties()
