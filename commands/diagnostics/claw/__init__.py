from commands2 import SequentialCommandGroup

from commands.diagnostics.claw.hascoral import DiagnoseHasCoral
from commands.diagnostics.claw.leftmotor import DiagnoseLeftMotor
from commands.diagnostics.claw.rightmotor import DiagnoseRightMotor
from subsystems.claw import Claw
from ultime.command import ignore_requirements


@ignore_requirements(["claw"])
class DiagnoseClaw(SequentialCommandGroup):
    def __init__(self, claw: Claw):
        super().__init__(
            DiagnoseHasCoral(claw), DiagnoseLeftMotor(claw), DiagnoseRightMotor(claw)
        )
