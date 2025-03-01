import math
from typing import Optional

from commands2 import Command
from robotpy_apriltag import AprilTagFieldLayout, AprilTagField
from wpilib import DriverStation
from wpimath.geometry import Pose2d, Rotation2d, Translation2d

from commands.drivetrain.drivetoposes import DriveToPoses
from subsystems.drivetrain import Drivetrain
from ultime.autoproperty import autoproperty
from ultime.command import DeferredCommand, ignore_requirements

tag_field = AprilTagFieldLayout.loadField(
    AprilTagField.k2025ReefscapeAndyMark
)


# Links the sextants to the corresponding AprilTag ID for each reef
alliance_to_sextant_to_tag_id = {
    DriverStation.Alliance.kBlue: {0: 21, 1: 20, 2: 19, 3: 18, 4: 17, 5: 22},
    DriverStation.Alliance.kRed: {0: 7, 1: 8, 2: 9, 3: 10, 4: 11, 5: 6},
}


alliance_to_reef_center = {
    DriverStation.Alliance.kBlue: Translation2d(4.56, 4.03),
    DriverStation.Alliance.kRed: Translation2d(13.04, 4.03),
}


tag_poses = {
    tag_id: tag_field.getTagPose(tag_id).toPose2d() for tag_id in [6, 7, 8, 9, 10, 11, 17, 18, 19, 20, 21, 22]
}


def getCurrentSextant(robot_position: Pose2d) -> Optional[int]:
    """
    Determines which sextant (0-5) of a hexagon contains a robot's position.
    The hexagon is oriented with a flat side on the right.
    Sextants are numbered counterclockwise, with 0 being the right-center sextant.

    Returns:
    int: Sextant number (0-5)
    """
    if DriverStation.getAlliance() is None:
        return None
    reef_position = alliance_to_reef_center[DriverStation.getAlliance()]

    dx = robot_position.X() - reef_position.X()
    dy = robot_position.Y() - reef_position.Y()

    # Calculate angle between robot and hexagon center, accounting for hexagon rotation
    # Add π/6 (30 degrees) to align with flat side orientation
    angle = math.atan2(dy, dx) + math.pi / 6
    angle = angle % (2 * math.pi)

    # Convert angle to sextant number (each sextant is 60 degrees = π/3 radians)
    sextant = int(angle / (math.pi / 3))
    return sextant


def getClosestReefTagID(robot_position: Pose2d) -> int:
    sextant = getCurrentSextant(robot_position)
    alliance = DriverStation.getAlliance()
    return alliance_to_sextant_to_tag_id[alliance][sextant]

@ignore_requirements(["drivetrain"])
class AlignWithReefSide(DeferredCommand):
    pose_offset = autoproperty(0.5)

    def __init__(self, drivetrain: Drivetrain):
        super().__init__()
        self.drivetrain = drivetrain

    def createCommand(self) -> Command:
        return DriveToPoses(
            self.drivetrain,
            [self.getTagPoseToAlign()],
        )

    def getTagPoseToAlign(self) -> Pose2d:
        tag = getClosestReefTagID(self.drivetrain.getPose())
        pose = tag_poses[tag]

        return self.offsetTagPositions(pose, self.pose_offset)

    @staticmethod
    def offsetTagPositions(tag_pos: Pose2d, offset_from_center: float):
        reef_center = alliance_to_reef_center[DriverStation.getAlliance()]

        # Get vector from reef center to tag position
        center_to_tag = tag_pos.translation() - reef_center
        # Scale unit vector by (original magnitude + offset)
        magnitude = center_to_tag.norm()
        end_vector = center_to_tag * ((magnitude + offset_from_center) / magnitude)

        return Pose2d(
            reef_center + end_vector,
            center_to_tag.angle() + Rotation2d.fromDegrees(180),
        )
