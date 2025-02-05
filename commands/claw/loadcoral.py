import wpilib

from subsystems.claw import Claw
from commands2 import Command
from commands.claw.drop import drop_properties

from ultime.autoproperty import autoproperty


class LoadCoral(Command):
    delay = autoproperty(0.7)

    def __init__(self, claw: Claw):
        super().__init__()
        self.claw = claw
        self.addRequirements(claw)
        self.timer = wpilib.Timer()

    def initialize(self):
        self.timer.restart()

    def execute(self):
        if self.claw.hasCoral():
            self.claw.setLeft(drop_properties.speed_level_2_left)
            self.claw.setRight(drop_properties.speed_level_2_right)
            if not self.claw.hasCoral():
                self.timer.start()
            print(self.claw.hasCoral())
        


    def isFinished(self) -> bool:
        return self.timer.get() >= self.delay

    def end(self, interrupted: bool):
        print(self.claw.hasCoral())
        self.claw.stop()

