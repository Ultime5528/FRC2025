from typing import List

from commands2 import SequentialCommandGroup, Command

from commands.resetall import ResetAll


class DiagnoseAll(SequentialCommandGroup):
    def __init__(self, hardware, components_tests: List[Command]):
        self._hardware = hardware
        super().__init__(
            ResetAll(self._hardware.elevator, self._hardware.printer, self._hardware.arm, self._hardware.intake,
                     self._hardware.climber),
            *components_tests
        )
