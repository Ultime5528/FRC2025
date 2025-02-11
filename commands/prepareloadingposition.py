from commands2 import ParallelCommandGroup

from commands.arm.retractarm import RetractArm
from commands.elevator.moveelevator import MoveElevator
from commands.printer.moveprinter import MovePrinter
from subsystems.arm import Arm
from subsystems.elevator import Elevator
from subsystems.printer import Printer


class PrepareLoadingPosition(ParallelCommandGroup):
    def __init__(self, elevator: Elevator, arm: Arm, printer: Printer):
        super().__init__(
            MoveElevator.toLoading(elevator),
            RetractArm(arm),
            MovePrinter.toLoading(printer),
        )
