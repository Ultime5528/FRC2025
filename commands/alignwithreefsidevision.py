import math
from typing import Union, Callable, Optional

from commands2.button import CommandXboxController
from photonlibpy.targeting import PhotonTrackedTarget
from robotpy_apriltag import AprilTagFieldLayout
from wpilib import DriverStation
from wpilib.interfaces import GenericHID
from wpimath.filter import SlewRateLimiter
from wpimath.geometry import Pose2d, Transform3d

from commands.drivetrain.drive import apply_center_distance_deadzone, properties
from subsystems.drivetrain import Drivetrain
from ultime.vision import RelativeVision
from ultime.autoproperty import autoproperty
from ultime.command import Command



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

# Links the sextants to the corresponding AprilTag ID for each reef
tag_id = {
    DriverStation.Alliance.kBlue: {0: 21, 1: 20, 2: 19, 3: 18, 4: 17, 5: 22},
    DriverStation.Alliance.kRed: {0: 7, 1: 8, 2: 9, 3: 10, 4: 11, 5: 6},
}

def getTagID(alliance: DriverStation.Alliance, sextant: int) -> int:
    return tag_id[alliance][sextant]



class AlignWithReefSideVision(Command):
    locating_rotation_speed = autoproperty(0.3)

    def __init__(
        self,
        drivetrain: Drivetrain,
        vision: RelativeVision,
        xbox_remote: Optional[CommandXboxController] = None,
    ):
        super().__init__()
        self.addRequirements(drivetrain)
        self.drivetrain = drivetrain
        self.vision = vision
        self.vel_rot = 0
        self.target: PhotonTrackedTarget = None
        self.m_xspeedLimiter = SlewRateLimiter(3)
        self.m_yspeedLimiter = SlewRateLimiter(3)
        self.tag_field = AprilTagFieldLayout("2025-reefscape-andymark.json")

    def execute(self):
        target_tag_id = getTagID(DriverStation.getAlliance(), getSextantFromPosition(self.drivetrain.getPose(), reef_centers[DriverStation.getAlliance()]))
        self.target: PhotonTrackedTarget = self.vision.getTargetWithID(target_tag_id)
        #
        # if self.target is not None:
        #     self.vel_rot = self.p * (self.horizontal_offset - self.target.getYaw())
        #     self.drivetrain.drive(
        #         x_speed, y_speed, self.vel_rot, is_field_relative=True
        #     )
        # else:
        robot_to_tag = self.tag_field.getTagPose(target_tag_id) - self.drivetrain.getPose()
        rotation_error = robot_to_tag.rotation().toRotation2d() - self.drivetrain.getPose().rotation()
        self.drivetrain.drive(0,0, math.copysign(self.locating_rotation_speed, rotation_error))


    def end(self, interrupted: bool):
        self.drivetrain.stop()
