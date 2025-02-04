from commands2 import Command
from wpilib import Timer

from subsystems.intake import Intake
from ultime.autoproperty import autoproperty


class DropAlgae(Command):
    drop_delay = autoproperty(5)

    def __init__(self, intake: Intake):
        super().__init__()
        self.intake = intake
        self.switch = self.intake.grab_switch
        self.timer = Timer()

    def initialize(self):
        self.timer.restart()

    def execute(self):
        self.intake.drop()

    def isFinished(self) -> bool:
        return self.timer.get() >= self.drop_delay

    def end(self, interrupted: bool):
        self.intake.stopGrab()
        self.timer.stop()