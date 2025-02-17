from commands2.cmd import sequence, either, none

from commands.claw.autodrop import AutoDrop
from commands.drivetrain.drivetoposes import DriveToPoses
from commands.elevator.moveelevator import MoveElevator
from commands.prepareloading import PrepareLoading
from commands.printer.moveprinter import MovePrinter
from subsystems.arm import Arm
from subsystems.claw import Claw
from subsystems.drivetrain import Drivetrain
from subsystems.elevator import Elevator
from subsystems.printer import Printer
from ultime.autoproperty import autoproperty


class DropPrepareLoading:
    @staticmethod
    def left(
        arm: Arm,
        claw: Claw,
        drivetrain: Drivetrain,
        elevator: Elevator,
        printer: Printer,
    ):
        cmd = sequence(
            MovePrinter.leftUntilReef(printer),
            AutoDrop(claw, elevator),
            either(
                sequence(
                    MoveElevator.toAlgae(elevator, arm),
                    DriveToPoses.back(drivetrain, lambda: _properties.distance_back),
                ),
                none(),
                lambda: arm.state == Arm.State.Extended,
            ),
            PrepareLoading(elevator, arm, printer),
        )
        cmd.setName(DropPrepareLoading.__name__ + ".left")
        return cmd

    @staticmethod
    def right(
        arm: Arm,
        claw: Claw,
        drivetrain: Drivetrain,
        elevator: Elevator,
        printer: Printer,
    ):

        cmd = sequence(
            MovePrinter.rightUntilReef(printer),
            AutoDrop(claw, elevator),
            either(
                sequence(
                    MoveElevator.toAlgae(elevator, arm),
                    DriveToPoses.back(drivetrain, lambda: _properties.distance_back),
                ),
                none(),
                lambda: arm.state == Arm.State.Extended,
            ),
            # TODO PrepareLoad()
        )
        cmd.setName(DropPrepareLoading.__name__ + ".right")
        return cmd


class _ClassProperties:
    distance_back = autoproperty(0.5, subtable=DropPrepareLoading.__name__)


_properties = _ClassProperties()
