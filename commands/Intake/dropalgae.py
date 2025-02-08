from commands2 import Command, SequentialCommandGroup
from wpilib import Timer

from commands.Intake.moveintake import MoveIntake
from subsystems.intake import Intake
from ultime.autoproperty import autoproperty


class DropAlgae(SequentialCommandGroup):
    def __init__(self, intake: Intake):
        super().__init__(_DropAlgae(intake), MoveIntake.toRetracted(intake))


class _DropAlgae(Command):
    drop_delay = autoproperty(3)

    def __init__(self, intake: Intake):
        super().__init__()
        self.intake = intake
        self.timer = Timer()

    def initialize(self):
        self.timer.restart()

    def execute(self):
        self.intake.drop()
        if self.intake.hasAlgae():
            self.timer.restart()

    def isFinished(self) -> bool:
        return self.timer.get() >= self.drop_delay

    def end(self, interrupted: bool):
        self.intake.stopGrab()
        self.timer.stop()
