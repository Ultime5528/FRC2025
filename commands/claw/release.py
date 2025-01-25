import wpilib
from commands2 import Command

from subsystems.claw import Claw
from ultime.autoproperty import autoproperty, FloatProperty, asCallable


class Drop(Command):

    speed_level_1_left = autoproperty(0.5)
    speed_level_1_right = autoproperty(0.0)
    speed_level_2_left = autoproperty(0.5)
    speed_level_2_right = autoproperty(0.5)
    speed_level_3_left = autoproperty(0.5)
    speed_level_3_right = autoproperty(0.5)
    speed_level_4_left = autoproperty(0.5)
    speed_level_4_right = autoproperty(0.5)
    delay = autoproperty(1.0)

    @classmethod
    def atLevel1(cls, claw: Claw):
        return cls(claw, Drop.speed_level_1_left, Drop.speed_level_1_right)

    @classmethod
    def atLevel2(cls, claw: Claw):
        return cls(claw, Drop.speed_level_2_left, Drop.speed_level_2_right)

    @classmethod
    def atLevel3(cls, claw: Claw):
        return cls(claw, Drop.speed_level_3_left, Drop.speed_level_3_right)

    @classmethod
    def atLevel4(cls, claw: Claw):
        return cls(claw, Drop.speed_level_4_left, Drop.speed_level_4_right)

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

    def initialize(self):
        speed_left = self.get_speed_left()
        self.claw.setLeft(speed_left)
        speed_right = self.get_speed_right()
        self.claw.setRight(speed_right)

        self.timer.reset()
        self.timer.start()

    def isFinished(self) -> bool:
        return self.timer.hasElapsed(self.delay)

    def end(self):
        self.claw.stop()
