from commands2 import SequentialCommandGroup
from wpilib import PowerDistribution

from commands.diagnostics.climber.switchandmotor import DiagnoseSwitchAndMotor
from subsystems.climber import Climber
from ultime.command import ignore_requirements


@ignore_requirements(["climber"])
class DiagnoseClimber(SequentialCommandGroup):
    def __init__(self, climber: Climber, pdp: PowerDistribution):
        super().__init__(
            DiagnoseSwitchAndMotor(climber, pdp),
        )
