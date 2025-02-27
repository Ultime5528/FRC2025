from _weakref import proxy
from typing import Optional, Callable

import commands2
import wpilib
from commands2 import Command
from pathplannerlib.auto import AutoBuilder, NamedCommands
from pathplannerlib.path import PathConstraints, PathPlannerPath
from wpimath.geometry import Pose2d

from commands.alignwithreefsidevision import AlignWithReefSideVision
from commands.arm.extendarm import ExtendArm
from commands.arm.retractarm import RetractArm
from commands.climber.resetclimber import ResetClimber
from commands.completedropsequence import CompleteDropSequence
from commands.elevator.moveelevator import MoveElevator
from commands.printer.moveprinter import MovePrinter
from commands.resetall import ResetAll
from commands.resetallbutclimber import ResetAllButClimber
from modules.hardware import HardwareModule
from ultime.followpath import FollowPath
from ultime.module import Module


def registerNamedCommand(command: Command):
    NamedCommands.registerCommand(command.getName(), command)


class AutonomousModule(Module):
    def __init__(self, hardware: HardwareModule):
        super().__init__()
        self.hardware = proxy(hardware)

        # AutoBuilder Configured with base PP functions. Only one that supports Pathfinding
        # Must test which AutoBuilder works best
        # AutoBuilder.configure(
        #     self.hardware.drivetrain.getPose,
        #     self.hardware.drivetrain.resetToPose,
        #     self.hardware.drivetrain.getRobotRelativeChassisSpeeds,
        #     self.hardware.drivetrain.driveFromChassisSpeeds,
        #     PPHolonomicDriveController(
        #         PIDConstants(5, 0, 0),
        #         PIDConstants(5, 0, 0),
        #     ),
        #     RobotConfig.fromGUISettings(),
        #     shouldFlipPath,
        #     self.hardware.drivetrain,
        # )

        # Flipping must be done by the command because the AutoBuilder uses custom code
        AutoBuilder.configureCustom(
            lambda path: FollowPath(path, self.hardware.drivetrain),
            lambda _: None,  # Disable resetOdometry
            True,
            lambda: False,  # Disable flipping, will be done by the command
        )

        self.setupCommandsOnPathPlanner()

        self.auto_command: Optional[commands2.Command] = None

        self.auto_chooser = AutoBuilder.buildAutoChooser()
        wpilib.SmartDashboard.putData("Autonomous mode", self.auto_chooser)

        self.auto_chooser.setDefaultOption("Nothing", None)

        self.hardware = hardware

    def setupCommandsOnPathPlanner(self):
        registerNamedCommand(AlignWithReefSideVision(self.hardware))
        registerNamedCommand(RetractArm(self.hardware.arm))
        registerNamedCommand(ExtendArm(self.hardware.arm))
        registerNamedCommand(ResetClimber(self.hardware.climber))
        registerNamedCommand(MoveElevator.toLevel4(self.hardware.elevator))
        registerNamedCommand(MoveElevator.toLevel1(self.hardware.elevator))
        registerNamedCommand(MoveElevator.toLevel2(self.hardware.elevator))
        registerNamedCommand(MovePrinter.toLoading(self.hardware.printer))
        registerNamedCommand(
            ResetAll(
                self.hardware.elevator,
                self.hardware.printer,
                self.hardware.arm,
                self.hardware.intake,
                self.hardware.climber,
            )
        )
        registerNamedCommand(
            ResetAllButClimber(
                self.hardware.elevator,
                self.hardware.printer,
                self.hardware.arm,
                self.hardware.intake,
            )
        )
        registerNamedCommand(
            CompleteDropSequence.toRight(
                self.hardware.printer,
                self.hardware.arm,
                self.hardware.elevator,
                self.hardware.drivetrain,
                self.hardware.claw,
            )
        )
        registerNamedCommand(
            CompleteDropSequence.toLeft(
                self.hardware.printer,
                self.hardware.arm,
                self.hardware.elevator,
                self.hardware.drivetrain,
                self.hardware.claw,
            )
        )

    def autonomousInit(self):
        self.auto_command: commands2.Command = self.auto_chooser.getSelected()
        if self.auto_command:
            self.auto_command.schedule()

    def autonomousExit(self):
        if self.auto_command:
            self.auto_command.cancel()

    def __del__(self):
        AutoBuilder._configured = False

        AutoBuilder._pathFollowingCommandBuilder: Callable[
            [PathPlannerPath], Command
        ] = None
        AutoBuilder._getPose: Callable[[], Pose2d] = None
        AutoBuilder._resetPose: Callable[[Pose2d], None] = None
        AutoBuilder._shouldFlipPath: Callable[[], bool] = None
        AutoBuilder._isHolonomic: bool = False

        AutoBuilder._pathfindingConfigured: bool = False
        AutoBuilder._pathfindToPoseCommandBuilder: Callable[
            [Pose2d, PathConstraints, float], Command
        ] = None
        AutoBuilder._pathfindThenFollowPathCommandBuilder: Callable[
            [PathPlannerPath, PathConstraints], Command
        ] = None

        NamedCommands._namedCommands = {}
