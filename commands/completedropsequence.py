from idlelib.debugobj import SequenceTreeItem
from typing import Literal

from commands2 import ConditionalCommand, SequentialCommandGroup

from commands.arm.retractarm import RetractArm
from commands.drivetrain.drivetoposes import DriveToPoses
from commands.elevator.moveelevator import MoveElevator
from commands.moveanddrop import MoveAndDrop
from commands.prepareloading import PrepareLoading
from subsystems.arm import Arm
from subsystems.claw import Claw
from subsystems.drivetrain import Drivetrain
from subsystems.elevator import Elevator
from subsystems.printer import Printer
from ultime.command import ignore_requirements


@ignore_requirements(["elevator", "printer", "arm", "intake", "claw", "drivetrain"])
class CompleteDropSequence(SequentialCommandGroup):
    @staticmethod
    def toLeft(printer: Printer, arm: Arm, elevator: Elevator, drivetrain: Drivetrain, claw: Claw):
        cmd = CompleteDropSequence(printer, arm, elevator, drivetrain, claw, "left")
        cmd.setName(CompleteDropSequence.__name__ + ".toLeft")
        return cmd

    @staticmethod
    def toRight(printer: Printer, arm: Arm, elevator: Elevator, drivetrain: Drivetrain, claw: Claw):
        cmd = CompleteDropSequence(printer, arm, elevator, drivetrain, claw, "right")
        cmd.setName(CompleteDropSequence.__name__ + ".toRight")
        return cmd

    def __init__(
            self,
            printer: Printer,
            arm: Arm,
            elevator: Elevator,
            drivetrain: Drivetrain,
            claw: Claw,
            side: Literal["right", "left"],
    ):
        super().__init__(
            ConditionalCommand(
                MoveAndDrop.toRight(printer, claw, elevator),
                MoveAndDrop.toLeft(printer, claw, elevator),
                lambda: side == "right",
            ),
            ConditionalCommand(
                SequentialCommandGroup(
                    MoveElevator.toAlgae(elevator, arm, drivetrain), DriveToPoses.back(drivetrain, 1),
                    RetractArm(arm),
                    PrepareLoading(elevator, arm, printer)
                ),
                SequentialCommandGroup(PrepareLoading(elevator, arm, printer)),
                lambda: arm.state == Arm.State.Extended,
            ),
        )
