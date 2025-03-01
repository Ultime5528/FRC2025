import math
from _weakref import proxy

from commands2 import Command, ScheduleCommand, DeferredCommand, SequentialCommandGroup
from robotpy_apriltag import AprilTagFieldLayout, AprilTagField
from wpilib import DriverStation, SmartDashboard
from wpimath.geometry import Pose2d, Rotation2d, Pose3d, Translation2d, Transform2d

from modules.diagnostics import DiagnosticsModule
from modules.hardware import HardwareModule
from ultime.autoproperty import autoproperty
from commands.drivetrain.drivetoposes import DriveToPoses

# Links the sextants to the corresponding AprilTag ID for each reef
tag_id = {
    DriverStation.Alliance.kBlue: {0: 21, 1: 20, 2: 19, 3: 18, 4: 17, 5: 22},
    DriverStation.Alliance.kRed: {0: 7, 1: 8, 2: 9, 3: 10, 4: 11, 5: 6},
}

reef_centers = {
    DriverStation.Alliance.kBlue: Translation2d(4.56, 4.03),
    DriverStation.Alliance.kRed: Translation2d(13.04, 4.03),
}

tag_pose = {
    6: Pose2d(Translation2d(x=13.474446, y=3.301238), Rotation2d(-1.047198)),
    7: Pose2d(Translation2d(x=13.890498, y=4.020820), Rotation2d(0.000000)),
    8: Pose2d(Translation2d(x=13.474446, y=4.740402), Rotation2d(1.047198)),
    9: Pose2d(Translation2d(x=12.643358, y=4.740402), Rotation2d(2.094395)),
    10: Pose2d(Translation2d(x=12.227306, y=4.020820), Rotation2d(3.141593)),
    11: Pose2d(Translation2d(x=12.643358, y=3.301238), Rotation2d(-2.094395)),
    17: Pose2d(Translation2d(x=4.073906, y=3.301238), Rotation2d(-2.094395)),
    18: Pose2d(Translation2d(x=3.657600, y=4.020820), Rotation2d(3.141593)),
    19: Pose2d(Translation2d(x=4.073906, y=4.740402), Rotation2d(2.094395)),
    20: Pose2d(Translation2d(x=4.904740, y=4.740402), Rotation2d(1.047198)),
    21: Pose2d(Translation2d(x=5.321046, y=4.020820), Rotation2d(0.000000)),
    22: Pose2d(Translation2d(x=4.904740, y=3.301238), Rotation2d(-1.047198))
}

def getCurrentSextant(robot_position: Pose2d) -> int:
    """
    Determines which sextant (0-5) of a hexagon contains a robot's position.
    The hexagon is oriented with a flat side on the right.
    Sextants are numbered counterclockwise, with 0 being the right-center sextant.

    Returns:
    int: Sextant number (0-5)
    """
    reef_position = reef_centers[DriverStation.getAlliance()]

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
    return tag_id[alliance][sextant]


class AlignWithReefSide(DeferredCommand):
    pose_offset = autoproperty(0.5)

    def __init__(self, hardware: HardwareModule):
        super().__init__(
            lambda: DriveToPoses(hardware.drivetrain, [self.getTagPoseToAlign(hardware.drivetrain.getPose())]),
            hardware.drivetrain,
        )
        self.hardware = hardware
        self.tag_field = AprilTagFieldLayout.loadField(
            AprilTagField.k2025ReefscapeAndyMark
        )

    def getTagPoseToAlign(self, robot_position: Pose2d) -> Pose2d:
        tag = getClosestReefTagID(robot_position)
        pose = tag_pose[tag]

        return self.offsetTagPositions(pose, self.pose_offset)

    @staticmethod
    def offsetTagPositions(tag_pos: Pose2d, offset_from_center: float):
        reef_center = reef_centers[DriverStation.getAlliance()]

        # Get vector from reef center to tag position
        center_to_tag = tag_pos.translation() - reef_center
        # Scale unit vector by (original magnitude + offset)
        magnitude = center_to_tag.norm()
        end_vector = center_to_tag * ((magnitude + offset_from_center) / magnitude)

        return Pose2d(
            reef_center + end_vector,
            center_to_tag   .angle() + Rotation2d.fromDegrees(180),
        )
