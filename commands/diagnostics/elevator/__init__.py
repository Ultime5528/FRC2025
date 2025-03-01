from commands2 import SequentialCommandGroup
from commands.diagnostics.elevator.ports import DiagnosePorts
from subsystems.elevator import Elevator


class DiagnoseElevator(SequentialCommandGroup):
    def __init__(self, elevator: Elevator):
        super().__init__(
            DiagnosePorts(elevator)
        )
