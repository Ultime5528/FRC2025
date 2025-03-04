from commands2 import SequentialCommandGroup

from commands.diagnostics.intake.extend import DiagnoseExtend
from commands.diagnostics.intake.hasalgae import DiagnoseHasAlgae
from commands.diagnostics.intake.retract import DiagnoseRetract
from subsystems.intake import Intake
from ultime.command import ignore_requirements


@ignore_requirements(["intake"])
class DiagnoseIntake(SequentialCommandGroup):
    def __init__(self, intake: Intake):
        super().__init__(
            DiagnoseHasAlgae(intake), DiagnoseExtend(intake), DiagnoseRetract(intake)
        )
