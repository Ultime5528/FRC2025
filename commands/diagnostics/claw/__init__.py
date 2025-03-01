from commands2 import SequentialCommandGroup

from commands.claw.loadcoral import LoadCoral
from commands.diagnostics.claw.droplevel4 import DiagnoseDropLevel4
from commands.diagnostics.claw.hascoral import DiagnoseHasCoral
from subsystems.claw import Claw
from ultime.command import ignore_requirements


@ignore_requirements(["claw"])
class DiagnoseClaw(SequentialCommandGroup):
    def __init__(self, claw: Claw):
        super().__init__(
            DiagnoseHasCoral(claw), LoadCoral(claw), DiagnoseDropLevel4(claw)
        )
