import wpilib
from commands2 import Command, SequentialCommandGroup
from wpilib import Timer

from commands.Intake.moveintake import MoveIntake
from subsystems.intake import Intake
from ultime.autoproperty import autoproperty


class GrabAlgae(SequentialCommandGroup):
    def __init__(self, intake: Intake):
        super().__init__(MoveIntake.toExtended(intake), _GrabAlgae(intake))


class _GrabAlgae(Command):
    grab_delay = autoproperty(5)

    def __init__(self, intake: Intake):
        super().__init__()
        self.intake = intake
        self.timer = Timer()

    def execute(self):
        if not self.intake.hasAlgae():
            self.intake.grab()
            self.timer.stop()
            self.timer.reset()
        else:
            self.timer.start()

    def isFinished(self) -> bool:
        return self.timer.get() >= self.grab_delay

    def end(self, interrupted: bool):
        self.intake.stopGrab()
        self.timer.stop()
