from typing import Literal

from commands2 import ConditionalCommand, SequentialCommandGroup

from commands.claw.autodrop import AutoDrop
from commands.printer.scanprinter import ScanPrinter
from modules.hardware import HardwareModule
from subsystems.claw import Claw
from subsystems.elevator import Elevator
from subsystems.printer import Printer
from ultime.command import ignore_requirements


@ignore_requirements(["printer", "claw"])
class MoveAndDrop(ConditionalCommand):
    @staticmethod
    def toLeft(printer: Printer, claw: Claw, elevator: Elevator):
        cmd = MoveAndDrop(
            printer,
            claw,
            elevator,
            "left"
        )
        cmd.setName(MoveAndDrop.__name__ + ".toLeft")
        return cmd

    @staticmethod
    def toRight(printer: Printer, claw: Claw, elevator: Elevator):
        cmd = MoveAndDrop(
            printer,
            claw,
            elevator,
            "right"
        )
        cmd.setName(MoveAndDrop.__name__ + ".toRight")
        return cmd

    def __init__(self, printer: Printer, claw: Claw, elevator: Elevator, side: Literal["right", "left"]):
        super().__init__(
            SequentialCommandGroup(
                ScanPrinter.right(printer),
                AutoDrop(claw, elevator)
            ),
            SequentialCommandGroup(
                ScanPrinter.left(printer),
                AutoDrop(claw, elevator)
            ),
            lambda: side == "right"
        )