from commands2 import SequentialCommandGroup
from commands2.cmd import parallel, sequence
from pathplannerlib.path import PathPlannerPath

from commands.claw.retractcoral import RetractCoral
from commands.elevator.moveelevator import MoveElevator
from commands.resetautonomous import ResetAutonomous
from modules.hardware import HardwareModule
from ultime.followpath import FollowPath


class MegaAutonomous(SequentialCommandGroup):
    def __init__(self, hardware: HardwareModule):
        super().__init__()

        reset_autonomous = ResetAutonomous(hardware.elevator, hardware.printer, hardware.arm)
        first_move_elevator_level4 = MoveElevator.toLevel4(hardware.elevator)
        retract_coral = RetractCoral.retract(hardware.claw)
        straight_align_22 = FollowPath(PathPlannerPath.fromPathFile("Straight Align #22"), hardware.drivetrain)

        self.addCommands(
            parallel(
                sequence(
                    reset_autonomous,
                    parallel(
                        first_move_elevator_level4,
                        retract_coral
                    )
                ),
                straight_align_22
            )
        )