from commands2 import ParallelCommandGroup, InstantCommand

from commands.elevator.resetelevator import ResetElevator
from commands.printer.resetprinter import ResetPrinterRight
from subsystems.arm import Arm
from subsystems.elevator import Elevator
from subsystems.printer import Printer
from ultime.command import ignore_requirements


@ignore_requirements(["elevator", "printer", "arm", "intake", "climber"])
class ResetAutonomous(ParallelCommandGroup):
    def __init__(
        self,
        elevator: Elevator,
        printer: Printer,
        arm: Arm,
    ):
        super().__init__(
            InstantCommand(lambda: arm.setReset()),
            ResetPrinterRight(printer),
            ResetElevator(elevator),
        )
