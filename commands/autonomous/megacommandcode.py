from commands2 import SequentialCommandGroup, ParallelCommandGroup
from commands2.cmd import parallel, sequence

from commands.drivetrain.drivetoposes import DriveToPoses, pose
from commands.elevator.moveelevator import MoveElevator
from commands.resetallbutclimber import ResetAllButClimber
from subsystems.arm import Arm
from subsystems.claw import Claw
from subsystems.climber import Climber
from subsystems.drivetrain import Drivetrain
from subsystems.elevator import Elevator
from subsystems.intake import Intake
from subsystems.printer import Printer

class MegaCommandCode(SequentialCommandGroup):
    def __init__(
        self,
        drivetrain: Drivetrain,
        arm : Arm,
        claw : Claw,
        elevator : Elevator,
        climber : Climber,
        printer : Printer,
        intake: Intake
    ):
        super().__init__(
            parallel(
            DriveToPoses.fromRedBluePoints(
                drivetrain,
                [
                    pose()
                ],
                [
                    pose(5.1359, 2.9006)
                ]
                ),
            sequence(
                ResetAllButClimber(elevator, printer, arm, intake),
                MoveElevator.toLevel1(elevator)),
                CompleteDropSequece.toRight

            ),

