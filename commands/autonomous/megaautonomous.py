from commands2 import SequentialCommandGroup
from commands2.cmd import parallel, sequence, either
from pathplannerlib.path import PathPlannerPath

from commands.claw.loadcoral import LoadCoral
from commands.claw.retractcoral import RetractCoral
from commands.claw.waituntilcoral import WaitUntilCoral
from commands.dropautonomous import DropAutonomous
from commands.elevator.moveelevator import MoveElevator
from commands.prepareloading import PrepareLoading
from commands.resetautonomous import ResetAutonomous
from modules.hardware import HardwareModule
from ultime.followpath import FollowPath


class MegaAutonomous(SequentialCommandGroup):
    @classmethod
    def left(cls, hardware: HardwareModule):
        cmd = MegaAutonomous(hardware, True)
        cmd.setName(MegaAutonomous.__name__ + ".left")
        return cmd

    @classmethod
    def right(cls, hardware: HardwareModule):
        cmd = MegaAutonomous(hardware, False)
        cmd.setName(MegaAutonomous.__name__ + ".right")
        return cmd

    def __init__(self, hardware: HardwareModule, is_left_side: bool):
        super().__init__()

        reset_autonomous = ResetAutonomous(
            hardware.elevator, hardware.printer, hardware.arm
        )

        first_move_elevator_level4 = MoveElevator.toLevel4(hardware.elevator)
        second_move_elevator_level4 = MoveElevator.toLevel4(hardware.elevator)

        first_retract_coral = RetractCoral.retract(hardware.claw)
        second_retract_coral = RetractCoral.retract(hardware.claw)

        straight_align_22_right = FollowPath(
            PathPlannerPath.fromPathFile("Straight Align #22 Right"),
            hardware.drivetrain,
        )
        straight_align_20_left = FollowPath(
            PathPlannerPath.fromPathFile("Straight Align #20 Left"), hardware.drivetrain
        )
        go_to_tag_17_after_coral_station_right = FollowPath(
            PathPlannerPath.fromPathFile("Go to tag #17 after loading Right"),
            hardware.drivetrain,
        )
        go_to_tag_19_after_coral_station_left = FollowPath(
            PathPlannerPath.fromPathFile("Go to tag #19 after loading Left"),
            hardware.drivetrain,
        )
        go_to_coral_station_after_tag_22_right = FollowPath(
            PathPlannerPath.fromPathFile("Go to Coral Station after reef #22 Right"),
            hardware.drivetrain,
        )
        go_to_coral_station_after_tag_20_left = FollowPath(
            PathPlannerPath.fromPathFile("Go to Coral Station after reef #20 Left"),
            hardware.drivetrain,
        )

        first_prepare_loading = PrepareLoading(
            hardware.elevator, hardware.arm, hardware.printer
        )
        load_coral = LoadCoral(hardware.claw, hardware.printer)
        wait_until_coral = WaitUntilCoral(hardware.claw)

        first_drop_autonomous = DropAutonomous.toRight(
            hardware.printer,
            hardware.arm,
            hardware.elevator,
            hardware.drivetrain,
            hardware.claw,
            True,
        )
        second_drop_autonomous = DropAutonomous.toRight(
            hardware.printer,
            hardware.arm,
            hardware.elevator,
            hardware.drivetrain,
            hardware.claw,
            True,
        )

        self.addCommands(
            parallel(
                sequence(
                    reset_autonomous,
                    parallel(first_move_elevator_level4, first_retract_coral),
                ),
                either(
                    straight_align_20_left,
                    straight_align_22_right,
                    lambda: is_left_side,
                ),
            ),
            first_drop_autonomous,
            parallel(
                either(
                    go_to_coral_station_after_tag_20_left,
                    go_to_coral_station_after_tag_22_right,
                    lambda: is_left_side,
                ),
                first_prepare_loading,
            ),
            wait_until_coral,
            load_coral,
            parallel(
                either(
                    go_to_tag_19_after_coral_station_left,
                    go_to_tag_17_after_coral_station_right,
                    lambda: is_left_side,
                ),
                second_move_elevator_level4,
                second_retract_coral,
            ),
            second_drop_autonomous,
        )
