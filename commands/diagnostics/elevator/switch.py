from commands2 import SequentialCommandGroup

from subsystems.elevator import Elevator
from ultime.command import ignore_requirements


@ignore_requirements(["elevator"])
class DiagnoseSwitch(SequentialCommandGroup):
    def __init__(self, elevator: Elevator):
        super().__init__(

        )

