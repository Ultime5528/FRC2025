from typing import List

from commands2 import SequentialCommandGroup, Command

from commands.resetall import ResetAll
from modules.hardware import HardwareModule


class DiagnoseAll(SequentialCommandGroup):
    def __init__(self, hardware: HardwareModule, components_tests: List[Command]):
        super().__init__(
            ResetAll(
                hardware.elevator,
                hardware.printer,
                hardware.arm,
                hardware.intake,
                hardware.climber,
            ),
            *components_tests
        )
