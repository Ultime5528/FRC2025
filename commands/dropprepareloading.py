from typing import Literal

import commands2
from commands2 import SequentialCommandGroup
from commands2.cmd import deadline

from commands.drivetrain.drive import DriveField
from commands.drivetrain.drivetoposes import DriveToPoses
from commands.dropautonomous import DropAutonomous
from commands.prepareloading import PrepareLoading
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
            DropAutonomous(printer, arm, elevator, drivetrain, claw, side),
            DriveToPoses.back(drivetrain, lambda: _properties.distance_end),
            deadline(
                PrepareLoading(elevator, arm, printer),
                DriveField(drivetrain, controller),
            ),
        )


class _ClassProperties:
    distance_remove_algae = autoproperty(0.7, subtable=DropPrepareLoading.__name__)
    distance_end = autoproperty(0.2, subtable=DropPrepareLoading.__name__)


_properties = _ClassProperties()
