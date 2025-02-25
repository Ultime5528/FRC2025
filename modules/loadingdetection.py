from commands2 import SequentialCommandGroup

from commands.claw.loadcoral import LoadCoral
from modules.hardware import HardwareModule
from ultime.module import Module
from commands.printer.moveprinter import MovePrinter

class LoadingDetection(Module):
    def __init__(self, hardware: HardwareModule):
        super().__init__()
        self.claw = hardware.claw
        self.elevator = hardware.elevator
        self.printer = hardware.printer
        self._load_command = LoadCoral(self.claw)

    def robotPeriodic(self) -> None:
        self.claw.is_at_loading = (
            self.printer.state == self.printer.State.Loading
            and self.elevator.state == self.elevator.State.Loading
        )

        if (
            self.claw.seesObject()
            and not self.claw.has_coral
            and self.claw.is_at_loading
        ):
            self._load_command.schedule()
