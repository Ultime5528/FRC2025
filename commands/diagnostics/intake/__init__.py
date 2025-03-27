from commands2 import SequentialCommandGroup
from wpilib import PowerDistribution

from commands.diagnostics.intake.extend import DiagnoseExtend
from commands.diagnostics.intake.grab import DiagnoseGrabMotor
from commands.diagnostics.intake.hasalgae import DiagnoseHasAlgae
from commands.diagnostics.intake.retract import DiagnoseRetract
from subsystems.intake import Intake
from ultime.command import ignore_requirements


@ignore_requirements(["intake"])
class DiagnoseIntake(SequentialCommandGroup):
    def __init__(self, intake: Intake, pdp: PowerDistribution):
        super().__init__(
            DiagnoseHasAlgae(intake),
            #DiagnoseExtend(intake, pdp),
            #DiagnoseRetract(intake),
            DiagnoseGrabMotor(intake, pdp),
        )
