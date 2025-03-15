from idlelib.debugger_r import gui_adap_oid

from commands2 import SequentialCommandGroup
from commands2.cmd import parallel, sequence
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
    def __init__(self, hardware: HardwareModule):
        super().__init__()

        reset_autonomous = ResetAutonomous(hardware.elevator, hardware.printer, hardware.arm)
        first_move_elevator_level4 = MoveElevator.toLevel4(hardware.elevator)
        first_retract_coral = RetractCoral.retract(hardware.claw)
        straight_align_22 = FollowPath(PathPlannerPath.fromPathFile("Straight Align #22"), hardware.drivetrain)
        first_drop_autonomous = DropAutonomous.toRight(hardware.printer, hardware.arm, hardware.elevator, hardware.drivetrain, hardware.claw, True)
        go_to_coral_station_after_tag_22 = FollowPath(PathPlannerPath.fromPathFile("Go to Coral Station after reef #22"), hardware.drivetrain)
        first_prepare_loading = PrepareLoading(hardware.elevator, hardware.arm, hardware.printer)
        wait_until_coral = WaitUntilCoral(hardware.claw)
        load_coral = LoadCoral(hardware.claw, hardware.printer)
        go_to_tag_17_after_coral_station = FollowPath(PathPlannerPath.fromPathFile("Go to tag #17 after loading"), hardware.drivetrain)
        second_move_elevator_level4 = MoveElevator.toLevel4(hardware.elevator)
        second_retract_coral = RetractCoral.retract(hardware.claw)
        second_drop_autonomous = DropAutonomous.toRight(hardware.printer, hardware.arm, hardware.elevator, hardware.drivetrain, hardware.claw, True)

        self.addCommands(
            parallel(
                sequence(
                    reset_autonomous,
                    parallel(
                        first_move_elevator_level4,
                        first_retract_coral
                    )
                ),
                straight_align_22
            ),
            first_drop_autonomous,
            parallel(
                go_to_coral_station_after_tag_22,
                first_prepare_loading
            ),
            wait_until_coral,
            load_coral,
            parallel(
                go_to_tag_17_after_coral_station,
                second_move_elevator_level4,
                second_retract_coral
            ),
            second_drop_autonomous
        )