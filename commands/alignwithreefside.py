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

from subsystems.drivetrain import Drivetrain

# Links the sextants to the corresponding AprilTag ID for each reef
tag_id = {
    DriverStation.Alliance.kBlue: {0: 21, 1: 20, 2: 19, 3: 18, 4: 17, 5: 22},
    DriverStation.Alliance.kRed: {0: 7, 1: 8, 2: 9, 3: 10, 4: 11, 5: 6},
}


def getSextantFromPosition(robot_position: Pose2d, hexagon_position: Pose2d) -> int:
    """
    Determines which sextant (0-5) of a hexagon contains a robot's position.
    The hexagon is oriented with a flat side on the right.
    Sextants are numbered counterclockwise, with 0 being the right-center sextant.

    Returns:
    int: Sextant number (0-5)
    """
    dx = robot_position.X() - hexagon_position.X()
    dy = robot_position.Y() - hexagon_position.Y()

    # Calculate angle between robot and hexagon center, accounting for hexagon rotation
    # Add π/6 (30 degrees) to align with flat side orientation
    angle = math.atan2(dy, dx) - hexagon_position.rotation().radians() + math.pi / 6
    angle = angle % (2 * math.pi)

    # Convert angle to sextant number (each sextant is 60 degrees = π/3 radians)
    sextant = int(angle / (math.pi / 3))
    return sextant


reef_centers = {
    DriverStation.Alliance.kBlue: Pose2d(4.56, 4.03, 0),
    DriverStation.Alliance.kRed: Pose2d(13.04, 4.03, 0),
}


class AlignWithReefSide(SequentialCommandGroup):
    def __init__(self, drivetrain: Drivetrain):
        super().__init__(
            DeferredCommand(
                lambda: AutoBuilder.pathfindToPose(
                    AprilTagFieldLayout(
                        r"C:\Users\First\Desktop\clone\FRC2025\2025-reefscape-andymark.json"
                    )
                    .getTagPose(
                        tag_id[DriverStation.getAlliance()][
                            getSextantFromPosition(
                                drivetrain.getPose(),
                                reef_centers[DriverStation.getAlliance()],
                            )
                        ]
                    )
                    .toPose2d()
                    .rotateBy(Rotation2d.fromDegrees(180)),
                    PathConstraints(3, 4, degreesToRadians(540), degreesToRadians(720)),
                ),
                drivetrain,
            )
        )
        self.addRequirements(drivetrain)
