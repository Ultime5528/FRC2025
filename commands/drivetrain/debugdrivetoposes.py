from typing import List, Callable

from commands2 import Command
from wpimath.geometry import Pose2d, Rotation2d

from commands.drivetrain.drivetoposes import DriveToPoses
from subsystems.drivetrain import Drivetrain

_goals = [
Pose2d(2.0, 4.0, Rotation2d.fromDegrees(0.0)),
Pose2d(2.0, 3.0, Rotation2d.fromDegrees(0.0)),
Pose2d(3.0, 3.0, Rotation2d.fromDegrees(0.0)),
Pose2d(4.0, 3.0, Rotation2d.fromDegrees(0.0)),
]

class DebugDriveToPoses(Command):
    @classmethod
    def oneGoal(cls, drivetrain: Drivetrain):
        cmd = DriveToPoses(
            drivetrain,
            _goals[:1],
        )
        cmd.setName(cmd.getName() + ".oneGoal")
        return cmd

class DebugDriveToPoses(Command):
        @classmethod
        def twoGoals(cls, drivetrain: Drivetrain):
            cmd = DriveToPoses(
                drivetrain,
                _goals[:2],
            )
            cmd.setName(cmd.getName() + ".twoGoals")
            return cmd

class DebugDriveToPoses(Command):
        @classmethod
        def threeGoals(cls, drivetrain: Drivetrain):
            cmd = DriveToPoses(
                drivetrain,
                _goals[:3],
            )
            cmd.setName(cmd.getName() + ".threeGoals")
            return cmd


class DebugDriveToPoses(Command):
    @classmethod
    def fourGoals(cls, drivetrain: Drivetrain):
        cmd = DriveToPoses(
            drivetrain,
            _goals[:4],
        )
        cmd.setName(cmd.getName() + ".fourGoals")
        return cmd

    def __init__(self):
        super().__init__()

    def isFinished(self) -> bool:
        return True
