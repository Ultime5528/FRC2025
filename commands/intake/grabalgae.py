from commands2 import Command, SequentialCommandGroup
from wpilib import Timer

from commands.intake.moveintake import MoveIntake
from subsystems.intake import Intake
from ultime.autoproperty import autoproperty
from ultime.command import ignore_requirements


@ignore_requirements(["intake"])
class GrabAlgae(SequentialCommandGroup):
    def __init__(self, intake: Intake):
        super().__init__(MoveIntake.toExtended(intake), _GrabAlgae(intake))


class _GrabAlgae(Command):
    delay = autoproperty(1.0, subtable=GrabAlgae.__name__)

    def __init__(self, intake: Intake):
        super().__init__()
        self.intake = intake
        self.addRequirements(intake)
        self.timer = Timer()

    def execute(self):
        self.intake.grab()

        if not self.intake.hasAlgae():
            self.timer.stop()
            self.timer.reset()
        else:
            self.timer.start()

    def isFinished(self) -> bool:
        return self.timer.get() >= self.delay

    def end(self, interrupted: bool):
        self.intake.stopGrab()
        self.timer.stop()
        self.timer.reset()
