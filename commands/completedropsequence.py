from typing import Literal

from commands2 import ConditionalCommand, SequentialCommandGroup, InstantCommand

from commands.claw.autodrop import AutoDrop
from commands.drivetrain.drivetoposes import DriveToPoses
from commands.elevator.moveelevator import MoveElevator
from commands.moveanddrop import MoveAndDrop
from commands.prepareloading import PrepareLoading
from subsystems.arm import Arm
from subsystems.claw import Claw
from subsystems.drivetrain import Drivetrain
from subsystems.elevator import Elevator
from subsystems.printer import Printer
from ultime.autoproperty import autoproperty
from ultime.command import ignore_requirements


@ignore_requirements(["elevator", "printer", "arm", "intake", "claw", "drivetrain"])
class CompleteDropSequence(SequentialCommandGroup):
    distance_remove_algae = autoproperty(0.5)

    @staticmethod
    def toLeft(
        printer: Printer,
        arm: Arm,
        elevator: Elevator,
        drivetrain: Drivetrain,
        claw: Claw,
    ):
        cmd = CompleteDropSequence(printer, arm, elevator, drivetrain, claw, "left")
        cmd.setName(CompleteDropSequence.__name__ + ".toLeft")
        return cmd

    @staticmethod
    def toRight(
        printer: Printer,
        arm: Arm,
        elevator: Elevator,
        drivetrain: Drivetrain,
        claw: Claw,
    ):
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
                AutoDrop(claw, elevator),
                SequentialCommandGroup(
                    # Check side
                    ConditionalCommand(
                        MoveAndDrop.toRight(printer, claw, elevator),
                        MoveAndDrop.toLeft(printer, claw, elevator),
                        lambda: side == "right",
                    ),
                    # Check if elevator is level 4 and arm extended (remove algae) if not, prepareloading
                    ConditionalCommand(
                        SequentialCommandGroup(
                            MoveElevator.toAlgae(elevator, drivetrain),
                            DriveToPoses.back(drivetrain, self.distance_remove_algae),
                        ),
                        InstantCommand(lambda: None, None),
                        lambda: elevator.state == Elevator.State.Level4
                        and arm.state == Arm.State.Extended,
                    ),
                ),
                lambda: elevator.state == Elevator.State.Level1,
            ),
            DriveToPoses.back(drivetrain, 0.1),
            PrepareLoading(elevator, arm, printer),
        )
