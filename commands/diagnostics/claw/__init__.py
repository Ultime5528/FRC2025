from commands2 import SequentialCommandGroup

from commands.diagnostics.claw.droplevel4 import DiagnoseDropLevel4
from commands.diagnostics.claw.hascoral import DiagnoseHasCoral
from commands.diagnostics.claw.load import DiagnoseLoad
from subsystems.claw import Claw


class DiagnoseClaw(SequentialCommandGroup):
    def __init__(self, claw: Claw):
        self.addRequirements(claw)
        super().__init__(
            DiagnoseHasCoral(claw), DiagnoseLoad(claw), DiagnoseDropLevel4(claw)
        )
