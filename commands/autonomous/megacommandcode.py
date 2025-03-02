from commands2 import SequentialCommandGroup
from commands2.cmd import parallel, sequence

from commands.arm.extendarm import ExtendArm
from commands.claw.waituntilcoral import WaitUntilCoral
from commands.climber.resetclimber import ResetClimber
from commands.drivetrain.drivetoposes import DriveToPoses, pose
from commands.dropprepareloading import DropPrepareLoading
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
        arm: Arm,
        claw: Claw,
        elevator: Elevator,
        climber: Climber,
        printer: Printer,
        intake: Intake,
    ):
        super().__init__(
            parallel(
                DriveToPoses.fromRedBluePoints(
                    drivetrain,
                    [pose(12.4127, 5.1311, -60.0)],
                    [pose(5.1359, 2.9006, 120.0)],
                ),
                sequence(
                    ResetAllButClimber(elevator, printer, arm, intake),
                    MoveElevator.toLevel2(elevator),
                ),
            ),
            DropPrepareLoading.toRight(),
            parallel(
                DriveToPoses.fromRedBluePoints(
                    drivetrain,
                    [pose(16.0406, 7.23474, 146.0)],
                    [pose(1.508, 0.797, -34.0)],
                ),
                ResetClimber(),
            ),
            WaitUntilCoral(claw),
            parallel(
                DriveToPoses.fromRedBluePoints(
                    drivetrain,
                    [pose(13.7059, 5.1310, -120.0)],
                    [pose(3.8427, 2.9008, 60.0)],
                ),
                MoveElevator.toLevel4(elevator),
                ExtendArm(arm),
            ),
            DropPrepareLoading.toRight(),
        )
