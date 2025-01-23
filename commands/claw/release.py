from idlelib.undo import Command

import wpilib

from subsystems.claw import Claw
from ultime.autoproperty import autoproperty


class ReleaseCoral(Command):

    speed_at_level_1 = autoproperty(0.5)
    speed_at_level_2 = autoproperty(0.5)
    speed_at_level_3 = autoproperty(0.5)
    speed_at_level_4 = autoproperty(0.5)

    @classmethod
    def dropAtLevel1(cls, claw: Claw):
        return cls(claw, )

    @classmethod
    def dropAtLevel2(cls, claw: Claw):
        return cls(claw, 1)

    @classmethod
    def dropAtLevel3(cls, claw: Claw):
        return cls(claw, 1)

    @classmethod
    def dropAtLevel4(cls, claw: Claw):
        return cls(claw, 1)

    def __init__(
            self,
            claw: Claw,
            speed: float,
    ):
        super().__init__()
        self.claw = claw
        self.timer = wpilib.Timer

    def execute(self):
        pass

    def isFinished(self) -> bool:
        pass

    def end(self):
        self.claw.stop()
