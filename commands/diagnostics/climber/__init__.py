from commands2 import SequentialCommandGroup

from commands.diagnostics.climber.switchandmotor import DiagnoseSwitchAndMotor
from subsystems.climber import Climber


class DiagnoseClimber(SequentialCommandGroup):
    def __init__(self, climber: Climber):
        super().__init__(
            DiagnoseSwitchAndMotor(climber),
        )
