import math

from commands2 import Command, ScheduleCommand, DeferredCommand, SequentialCommandGroup
from pathplannerlib.auto import AutoBuilder
from pathplannerlib.commands import PathfindingCommand
from pathplannerlib.path import PathConstraints
from pathplannerlib.pathfinders import Pathfinder
from pathplannerlib.pathfinding import Pathfinding
from robotpy_apriltag import AprilTagFieldLayout
from wpilib import DriverStation
from wpimath.geometry import Pose2d, Rotation2d, Pose3d, Translation2d
from wpimath.units import degreesToRadians

from modules.autonomous import AutonomousModule
from subsystems.drivetrain import Drivetrain

class AlignWithReefSide(DeferredCommand):
    def __init__(self, drivetrain: Drivetrain, autonomous: AutonomousModule):
        super().__init__(
            lambda: AutoBuilder.pathfindToPose(
                self.autonomous.getTagPoseToAlign(),
                PathConstraints(
                    3.0, 4.0,
                    degreesToRadians(540), degreesToRadians(720)
                )
            ), self._hardware.drivetrain
        )