from commands2 import SequentialCommandGroup
from commands2.cmd import parallel, sequence, either, waitSeconds
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

        move_elevator_level4_1 = MoveElevator.toLevel3(hardware.elevator)
        move_elevator_level4_2 = MoveElevator.toLevel4(hardware.elevator)
        move_elevator_level4_3 = MoveElevator.toLevel4(hardware.elevator)

        retract_coral_1 = RetractCoral.retract(hardware.claw)
        retract_coral_2 = RetractCoral.retract(hardware.claw)
        retract_coral_3 = RetractCoral.retract(hardware.claw)

        straight_align_22_right = FollowPath(
            PathPlannerPath.fromPathFile("Straight Align #22 Right"),
            hardware.drivetrain,
        )
        straight_align_20_left = FollowPath(
            PathPlannerPath.fromPathFile("Straight Align #20 Left"), hardware.drivetrain
        )


        go_to_tag_17_after_coral_station_right_1 = FollowPath(
            PathPlannerPath.fromPathFile("Go to tag #17 after loading Right"),
            hardware.drivetrain,
        )
        go_to_tag_19_after_coral_station_left_1 = FollowPath(
            PathPlannerPath.fromPathFile("Go to tag #19 after loading Left"),
            hardware.drivetrain,
        )
        go_to_tag_17_after_coral_station_right_2 = FollowPath(
            PathPlannerPath.fromPathFile("Go to tag #17 after loading Right"),
            hardware.drivetrain,
        )
        go_to_tag_19_after_coral_station_left_2 = FollowPath(
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
        go_to_coral_station_after_tag_17_right = FollowPath(
            PathPlannerPath.fromPathFile("Go to Coral Station after reef #17 Right"),
            hardware.drivetrain,
        )
        go_to_coral_station_after_tag_19_left = FollowPath(
            PathPlannerPath.fromPathFile("Go to Coral Station after reef #19 Left"),
            hardware.drivetrain,
        )

        prepare_loading_1 = PrepareLoading(
            hardware.elevator, hardware.arm, hardware.printer
        )
        load_coral_1 = LoadCoral(hardware.claw, hardware.printer)
        wait_until_coral_1 = WaitUntilCoral(hardware.claw)

        prepare_loading_2 = PrepareLoading(
            hardware.elevator, hardware.arm, hardware.printer
        )
        load_coral_2 = LoadCoral(hardware.claw, hardware.printer)
        wait_until_coral_2 = WaitUntilCoral(hardware.claw)

        drop_auto_1 = DropAutonomous(
            hardware.printer,
            hardware.arm,
            hardware.elevator,
            hardware.drivetrain,
            hardware.claw,
            "none",
            True,
        )
        drop_auto_2 = DropAutonomous(
            hardware.printer,
            hardware.arm,
            hardware.elevator,
            hardware.drivetrain,
            hardware.claw,
            "none",
            True,
        )
        drop_auto_3 = DropAutonomous(
            hardware.printer,
            hardware.arm,
            hardware.elevator,
            hardware.drivetrain,
            hardware.claw,
            "none",
            True,
        )

        self.addCommands(
            parallel(
                sequence(
                    reset_autonomous,
                    parallel(move_elevator_level4_1, retract_coral_1),
                ),
                either(
                    straight_align_20_left,
                    straight_align_22_right,
                    lambda: is_left_side,
                ),
            ),
            drop_auto_1,
            #coral 2
            parallel(
                either(
                    go_to_coral_station_after_tag_20_left,
                    go_to_coral_station_after_tag_22_right,
                    lambda: is_left_side,
                ),
                prepare_loading_1,
            ),
            wait_until_coral_1,
            parallel(
                sequence(
                    load_coral_1,
                    retract_coral_2,
                ),
                sequence(
                    parallel(
                        either(
                            go_to_tag_19_after_coral_station_left_1,
                            go_to_tag_17_after_coral_station_right_1,
                            lambda: is_left_side,
                        ),
                        sequence(
                            waitSeconds(0.3),
                            move_elevator_level4_2,
                        )
                    ),
                )
            ),
            drop_auto_2,
            #Coral 3
            parallel(
                either(
                    go_to_coral_station_after_tag_19_left,
                    go_to_coral_station_after_tag_17_right,
                    lambda: is_left_side,
                ),
                prepare_loading_2,
            ),
            wait_until_coral_2,
            parallel(
                sequence(
                    load_coral_2,
                    retract_coral_3,
                ),
                sequence(
                    parallel(
                        either(
                            go_to_tag_19_after_coral_station_left_2,
                            go_to_tag_17_after_coral_station_right_2,
                            lambda: is_left_side,
                        ),
                        sequence(
                            waitSeconds(0.3),
                            move_elevator_level4_3,
                        )
                    ),
                )
            ),
        )
