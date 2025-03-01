from commands2 import SequentialCommandGroup

from commands.claw.drop import Drop
from commands.claw.loadcoral import LoadCoral
from subsystems.claw import Claw
from ultime.command import ignore_requirements


@ignore_requirements(["claw"])
class DiagnoseLoad(SequentialCommandGroup):
    def __init__(self, claw: Claw):
        super().__init__(LoadCoral(claw))
        self.claw = claw

    def end(self, interrupted: bool):
        super().end(interrupted)
