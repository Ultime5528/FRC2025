from typing import Literal

import commands2
from commands2 import SequentialCommandGroup
from commands2.cmd import sequence, either, none, race

from commands.claw.autodrop import AutoDrop
from commands.drivetrain.drive import DriveField
from commands.drivetrain.drivetoposes import DriveToPoses
from commands.elevator.moveelevator import MoveElevator
from commands.prepareloading import PrepareLoading
from commands.printer.moveprinter import MovePrinter
from commands.printer.scanprinter import ScanPrinter
from subsystems.arm import Arm
from subsystems.claw import Claw
from subsystems.drivetrain import Drivetrain
from subsystems.elevator import Elevator
from subsystems.printer import Printer
from ultime.autoproperty import autoproperty
from ultime.command import ignore_requirements


@ignore_requirements(["elevator", "printer", "arm", "intake", "claw", "drivetrain"])
class DropPrepareLoading(SequentialCommandGroup):
    @staticmethod
    def toLeft(
        printer: Printer,
        arm: Arm,
        elevator: Elevator,
        drivetrain: Drivetrain,
        claw: Claw,
        controller: commands2.button.commandxboxcontroller,
    ):
        cmd = DropPrepareLoading(
            printer, arm, elevator, drivetrain, claw, controller, "left"
        )
        cmd.setName(DropPrepareLoading.__name__ + ".toLeft")
        return cmd

    @staticmethod
    def toRight(
        printer: Printer,
        arm: Arm,
        elevator: Elevator,
        drivetrain: Drivetrain,
        claw: Claw,
        controller: commands2.button.commandxboxcontroller,
    ):
        cmd = DropPrepareLoading(
            printer, arm, elevator, drivetrain, claw, controller, "right"
        )
        cmd.setName(DropPrepareLoading.__name__ + ".toRight")
        return cmd

    def __init__(
        self,
        printer: Printer,
        arm: Arm,
        elevator: Elevator,
        drivetrain: Drivetrain,
        claw: Claw,
        controller: commands2.button.commandxboxcontroller,
        side: Literal["right", "left"],
    ):
        super().__init__(
            either(
                sequence(
                    MovePrinter.toMiddle(printer),
                    AutoDrop(claw, elevator),
                ),
                sequence(
                    # Check side
                    (
                        ScanPrinter.right(printer)
                        if side == "right"
                        else ScanPrinter.left(printer)
                    ),
                    AutoDrop(claw, elevator),
                    # Check if elevator is level 4 and arm extended (remove algae) if not, prepare loading
                    either(
                        sequence(
                            MoveElevator.toAlgae(elevator, drivetrain),
                            DriveToPoses.back(
                                drivetrain, lambda: _properties.distance_remove_algae
                            ),
                        ),
                        none(),
                        lambda: elevator.state == Elevator.State.Level4
                        and arm.state == Arm.State.Extended,
                    ),
                ),
                lambda: elevator.state == Elevator.State.Level1,
            ),
            DriveToPoses.back(drivetrain, lambda: _properties.distance_end),
            race(
                PrepareLoading(elevator, arm, printer),
                DriveField(drivetrain, controller),
            ),
        )


class _ClassProperties:
    distance_remove_algae = autoproperty(0.7, subtable=DropPrepareLoading.__name__)
    distance_end = autoproperty(0.2, subtable=DropPrepareLoading.__name__)


_properties = _ClassProperties()
