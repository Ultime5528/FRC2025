from _weakref import proxy
from typing import Optional, Callable

import commands2
import wpilib
from commands2 import Command
from pathplannerlib.auto import AutoBuilder, NamedCommands
from pathplannerlib.path import PathConstraints, PathPlannerPath
from pathplannerlib.pathfinding import Pathfinding
from wpimath.geometry import Pose2d

from commands.arm.retractarm import RetractArm
from commands.elevator.moveelevator import MoveElevator
from commands.printer.moveprinter import MovePrinter
from commands.resetall import ResetAll
from modules.hardware import HardwareModule
from ultime.module import Module


def registerNamedCommand(command: Command):
    NamedCommands.registerCommand(command.getName(), command)


class AutonomousModule(Module):
    def robotInit(self) -> None:
        Pathfinding.ensureInitialized()

    def __init__(self, hardware: HardwareModule):
        super().__init__()
        self.hardware = proxy(hardware)

        self.setupCommandsOnPathPlanner()

        self.auto_command: Optional[commands2.Command] = None

        self.auto_chooser = AutoBuilder.buildAutoChooser()
        wpilib.SmartDashboard.putData("Autonomous mode", self.auto_chooser)

        self.auto_chooser.setDefaultOption("Nothing", None)

    def setupCommandsOnPathPlanner(self):
        registerNamedCommand(RetractArm(self.hardware.arm))
        registerNamedCommand(MoveElevator.toLevel1(self.hardware.elevator))
        registerNamedCommand(MovePrinter.toLoading(self.hardware.printer))
        registerNamedCommand(ResetAll(self.hardware.elevator, self.hardware.printer, self.hardware.arm, self.hardware.intake, self.hardware.climber))

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
