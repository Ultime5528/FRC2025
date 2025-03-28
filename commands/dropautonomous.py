from typing import Literal

from commands2 import SequentialCommandGroup
from commands2.cmd import sequence, either, none, deadline
from wpimath.geometry import Translation2d

from commands.claw.autodrop import AutoDrop
from commands.drivetrain.driverelative import DriveRelative
from commands.drivetrain.drivetoposes import DriveToPoses
from commands.elevator.maintainelevator import MaintainElevator
from commands.elevator.moveelevator import MoveElevator
from commands.printer.moveprinter import MovePrinter
from commands.printer.scanprinter import ScanPrinter
from subsystems.arm import Arm
from subsystems.claw import Claw
from subsystems.drivetrain import Drivetrain
from subsystems.elevator import Elevator
from subsystems.printer import Printer
from ultime.autoproperty import autoproperty
from ultime.command import ignore_requirements


@ignore_requirements(["elevator", "printer", "arm", "claw", "drivetrain"])
class DropAutonomous(SequentialCommandGroup):
    @staticmethod
    def toLeft(
        printer: Printer,
        arm: Arm,
        elevator: Elevator,
        drivetrain: Drivetrain,
        claw: Claw,
        always_drop: bool,
    ):
        cmd = DropAutonomous(
            printer, arm, elevator, drivetrain, claw, "left", always_drop
        )
        cmd.setName(DropAutonomous.__name__ + ".toLeft")
        return cmd

    @staticmethod
    def toRight(
        printer: Printer,
        arm: Arm,
        elevator: Elevator,
        drivetrain: Drivetrain,
        claw: Claw,
        always_drop: bool,
    ):
        cmd = DropAutonomous(
            printer, arm, elevator, drivetrain, claw, "right", always_drop
        )
        cmd.setName(DropAutonomous.__name__ + ".toRight")
        return cmd

    def __init__(
        self,
        printer: Printer,
        arm: Arm,
        elevator: Elevator,
        drivetrain: Drivetrain,
        claw: Claw,
        side: Literal["right", "left", "none"],
        always_drop: bool,
    ):
        super().__init__(
            either(
                deadline(
                    sequence(
                        MovePrinter.toMiddle(printer),
                        AutoDrop(claw, elevator),
                    ),
                    MaintainElevator(elevator),
                    DriveRelative(drivetrain, Translation2d(0.12, 0)),
                ),
                sequence(
                    deadline(
                        # Check side
                        (
                            {
                                "right": ScanPrinter.right(printer),
                                "left": ScanPrinter.left(printer),
                                "none": none(),
                            }[side]
                        ),
                        MaintainElevator(elevator),
                        DriveRelative(drivetrain, Translation2d(0.12, 0)),
                    ),
                    either(
                        sequence(
                            deadline(
                                AutoDrop(claw, elevator),
                                MaintainElevator(elevator),
                                DriveRelative(drivetrain, Translation2d(0.12, 0)),
                            ),
                            either(
                                sequence(
                                    MoveElevator.toAlgae(elevator, drivetrain),
                                    DriveToPoses.back(
                                        drivetrain,
                                        lambda: _properties.distance_remove_algae,
                                    ),
                                ),
                                none(),
                                lambda: elevator.state == Elevator.State.Level4
                                and arm.state == Arm.State.Extended,
                            ),
                        ),
                        none(),
                        lambda: always_drop or printer.scanned,
                    ),
                    # Check if elevator is level 4 and arm extended (remove algae) if not, prepare loading
                ),
                lambda: elevator.state == Elevator.State.Level1,
            ),
        )


class _ClassProperties:
    distance_remove_algae = autoproperty(0.7, subtable=DropAutonomous.__name__)
    distance_end = autoproperty(0.2, subtable=DropAutonomous.__name__)


_properties = _ClassProperties()
