import math
from _weakref import proxy
from typing import Optional, Callable

import commands2
import wpilib
from commands2 import Command
from pathplannerlib.auto import AutoBuilder, NamedCommands
from pathplannerlib.path import PathConstraints, PathPlannerPath
from pathplannerlib.pathfinding import Pathfinding
from robotpy_apriltag import AprilTagFieldLayout
from wpilib import DriverStation
from wpimath.geometry import Pose2d, Rotation2d

from commands.arm.retractarm import RetractArm
from commands.elevator.moveelevator import MoveElevator
from commands.printer.moveprinter import MovePrinter
from modules.hardware import HardwareModule
from ultime.module import Module


def registerNamedCommand(command: Command):
    NamedCommands.registerCommand(command.getName(), command)


class AutonomousModule(Module):
    def __init__(self, hardware: HardwareModule):
        super().__init__()

        self.auto_command: Optional[commands2.Command] = None

        self.auto_chooser = wpilib.SendableChooser()
        wpilib.SmartDashboard.putData("Autonomous mode", self.auto_chooser)

        self.auto_chooser.setDefaultOption("Nothing", None)

        self.hardware = hardware

        self.tag_field = AprilTagFieldLayout(r"C:\Users\First\Desktop\clone\FRC2025\2025-reefscape-andymark.json")

    def setupCommandsOnPathPlanner(self):
        registerNamedCommand(RetractArm(self.hardware.arm))
        registerNamedCommand(MoveElevator.toLevel1(self.hardware.elevator))
        registerNamedCommand(MovePrinter.toLoading(self.hardware.printer))



    def autonomousInit(self):
        self.auto_command: commands2.Command = self.auto_chooser.getSelected()
        if self.auto_command:
            self.auto_command.schedule()

    def autonomousExit(self):
        if self.auto_command:
            self.auto_command.cancel()
