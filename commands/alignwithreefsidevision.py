import math
from _weakref import proxy

from commands2 import Command, ScheduleCommand, DeferredCommand, SequentialCommandGroup
from pathplannerlib.auto import AutoBuilder
from pathplannerlib.commands import PathfindingCommand
from pathplannerlib.path import PathConstraints
from pathplannerlib.pathfinders import Pathfinder
from pathplannerlib.pathfinding import Pathfinding
from robotpy_apriltag import AprilTagFieldLayout, AprilTagField
from wpilib import DriverStation, SmartDashboard
from wpimath._controls._controls.trajectory import Trajectory
from wpimath.geometry import Pose2d, Rotation2d, Pose3d, Translation2d, Transform2d
from wpimath.units import degreesToRadians

from modules.autonomous import AutonomousModule
from modules.hardware import HardwareModule
from subsystems.drivetrain import Drivetrain
from ultime.autoproperty import autoproperty
from commands.drivetrain.drivetoposes import DriveToPoses

# Links the sextants to the corresponding AprilTag ID for each reef
tag_id = {
    DriverStation.Alliance.kBlue: {0: 21, 1: 20, 2: 19, 3: 18, 4: 17, 5: 22},
    DriverStation.Alliance.kRed: {0: 7, 1: 8, 2: 9, 3: 10, 4: 11, 5: 6},
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
    DriverStation.Alliance.kRed: Pose2d(13.04, 4.03, 0),
}


def getTagID(alliance: DriverStation.Alliance, sextant: int) -> int:
    return tag_id[alliance][sextant]


class AlignWithReefSideVision(DeferredCommand):
    pose_offset = autoproperty(0.5)

    def __init__(self, hardware: HardwareModule):
        super().__init__(
            lambda: DriveToPoses(hardware.drivetrain, [self.getTagPoseToAlign()]),
            hardware.drivetrain,
        )
        self.hardware = proxy(hardware)
        self.tag_field = AprilTagFieldLayout.loadField(
            AprilTagField.k2025ReefscapeAndyMark
        )

    def getTagPoseToAlign(self) -> Pose2d:
        pose = self.tag_field.getTagPose(
            getTagID(
                DriverStation.getAlliance(),
                getSextantFromPosition(
                    self.hardware.drivetrain.getPose(),
                    reef_centers[DriverStation.getAlliance()],
                ),
            )
        ).toPose2d()

        return self.offsetTagPositions(pose, self.pose_offset)

    @staticmethod
    def offsetTagPositions(tag_pos: Pose2d, offset_from_center: float):
        # Get vector from reef center to tag position
        tag_vector: Translation2d = (
            tag_pos - reef_centers[DriverStation.getAlliance()]
        ).translation()

        # Convert to unit vector by dividing by magnitude
        vector_magnitude = math.sqrt(tag_vector.X() ** 2 + tag_vector.Y() ** 2)
        unit_vector = Transform2d(
            tag_vector.X() / vector_magnitude, tag_vector.Y() / vector_magnitude, 0
        )

        # Scale unit vector by (original magnitude + offset)
        end_vector = unit_vector * (vector_magnitude + offset_from_center)
        reef_center = reef_centers[DriverStation.getAlliance()]
        return Pose2d(
            end_vector.X() + reef_center.X(),
            end_vector.Y() + reef_center.Y(),
            tag_vector.angle().rotateBy(Rotation2d.fromDegrees(180)),
        )
