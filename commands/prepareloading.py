from commands2 import ParallelCommandGroup, SequentialCommandGroup
from commands2.cmd import either, none

from commands.arm.retractarm import RetractArm
from commands.elevator.moveelevator import MoveElevator
from commands.printer.moveprinter import MovePrinter
from subsystems.arm import Arm
from subsystems.elevator import Elevator
from subsystems.printer import Printer
from ultime.command import ignore_requirements


@ignore_requirements(["elevator", "arm", "printer"])
class PrepareLoading(ParallelCommandGroup):
    def __init__(self, elevator: Elevator, arm: Arm, printer: Printer):
        super().__init__(
            MoveElevator.toLoading(elevator),
            either(
                none(),
                RetractArm(arm),
                lambda: arm.state == Arm.State.Retracted,
            ),
            MovePrinter.toLoading(printer),
        )
