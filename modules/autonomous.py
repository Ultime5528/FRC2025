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


# Links the sextants to the corresponding AprilTag ID for each reef
tag_id = {
    DriverStation.Alliance.kBlue: {
        0: 21,
        1: 20,
        2: 19,
        3: 18,
        4: 17,
        5: 22
    },
    DriverStation.Alliance.kRed: {
        0: 7,
        1: 8,
        2: 9,
        3: 10,
        4: 11,
        5: 6
    }
}


def getSextantFromPosition(robot_position: Pose2d, reef_position: Pose2d) -> int:
    """
    Determines which sextant (0-5) of a hexagon contains a robot's position.
    The hexagon is oriented with a flat side on the right.
    Sextants are numbered counterclockwise, with 0 being the right-center sextant.

    Returns:
    int: Sextant number (0-5)
    """
    dx = robot_position.X() - reef_position.X()
    dy = robot_position.Y() - reef_position.Y()

    # Calculate angle between robot and hexagon center, accounting for hexagon rotation
    # Add π/6 (30 degrees) to align with flat side orientation
    angle = math.atan2(dy, dx) - reef_position.rotation().radians() + math.pi / 6
    angle = angle % (2 * math.pi)

    # Convert angle to sextant number (each sextant is 60 degrees = π/3 radians)
    sextant = int(angle / (math.pi / 3))
    return sextant


reef_centers = {
    DriverStation.Alliance.kBlue: Pose2d(4.56, 4.03, 0),
    DriverStation.Alliance.kRed: Pose2d(13.04, 4.03, 0)
}


def getTagID(alliance: DriverStation.Alliance, sextant: int) -> int:
    return tag_id[alliance][sextant]


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

    def getTagPoseToAlign(self) -> Pose2d:
        return (self.tag_field.getTagPose(
            getTagID(DriverStation.getAlliance(), getSextantFromPosition(self.hardware.drivetrain.getPose(),
                                                                         reef_centers[DriverStation.getAlliance()]))
        ).toPose2d())

    def autonomousInit(self):
        self.auto_command: commands2.Command = self.auto_chooser.getSelected()
        if self.auto_command:
            self.auto_command.schedule()

    def autonomousExit(self):
        if self.auto_command:
            self.auto_command.cancel()
