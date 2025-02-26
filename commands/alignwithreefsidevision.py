from typing import Union, Callable, Optional

from commands2.button import CommandXboxController
from photonlibpy.targeting import PhotonTrackedTarget
from wpilib import DriverStation
from wpilib.interfaces import GenericHID
from wpimath.filter import SlewRateLimiter

from commands.drivetrain.drive import apply_center_distance_deadzone, properties
from subsystems.drivetrain import Drivetrain
from modules.relativetagvision import RelativeTagVisionModule
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


def getTagID(alliance: DriverStation.Alliance, sextant: int) -> int:
    return tag_id[alliance][sextant]



class AlignWithReefSideVision(Command):
    p = autoproperty(0.025)
    horizontal_offset = autoproperty(0.0)

    def __init__(
        self,
        drivetrain: Drivetrain,
        vision: RelativeTagVisionModule,
        xbox_remote: Optional[CommandXboxController] = None,
    ):
        super().__init__()
        self.addRequirements(drivetrain)
        self.drivetrain = drivetrain
        self.vision = vision
        self.xbox_remote = xbox_remote
        self.hid = xbox_remote.getHID() if xbox_remote else None
        self.vel_rot = 0
        self.target:PhotonTrackedTarget = None
        self.m_xspeedLimiter = SlewRateLimiter(3)
        self.m_yspeedLimiter = SlewRateLimiter(3)

    def execute(self):
        self.target = self.vision.getTagFromID(getTagID(DriverStation.getAlliance(), getSextantFromPosition(self.drivetrain.getPose(), reef_centers[DriverStation.getAlliance()])))

        if self.xbox_remote:
            x_speed, y_speed, _ = apply_center_distance_deadzone(
                self.xbox_remote.getLeftY() * -1,
                self.xbox_remote.getLeftX() * -1,
                properties.moving_deadzone,
            )
            x_speed = self.m_xspeedLimiter.calculate(x_speed)
            y_speed = self.m_yspeedLimiter.calculate(y_speed)

            if DriverStation.getAlliance() == DriverStation.Alliance.kRed:
                x_speed *= -1
                y_speed *= -1

        else:
            x_speed = 0.0
            y_speed = 0.0

        if self.target is not None:
            self.vel_rot = self.p * (self.horizontal_offset - self.target.getYaw())
            self.drivetrain.drive(
                x_speed, y_speed, self.vel_rot, is_field_relative=True
            )
        elif self.hid:
            self.drivetrain.drive(x_speed, y_speed, 0, is_field_relative=True)
            self.hid.setRumble(GenericHID.RumbleType.kBothRumble, 1.0)

    def end(self, interrupted: bool):
        self.drivetrain.stop()
        if self.hid:
            self.hid.setRumble(GenericHID.RumbleType.kBothRumble, 0)