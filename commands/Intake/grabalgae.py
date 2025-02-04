import wpilib
from commands2 import Command
from wpilib import Timer

from subsystems.intake import Intake


class GrabAlgae(Command):
    def __init__(self, intake: Intake):
        super().__init__()
        self.intake = intake
        self.switch = self.intake.grab_switch
        self.timer = Timer()

    def execute(self):
        if not self.switch.isPressed():
            self.intake.grab()
            self.timer.stop()
        else:
            self.timer.restart()

    def isFinished(self) -> bool:
        return self.timer.get() >= self.intake.grab_delay

    def end(self, interrupted: bool):
        self.intake.stopGrab()
        self.timer.stop()

