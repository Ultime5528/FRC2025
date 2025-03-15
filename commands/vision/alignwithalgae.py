from typing import Optional

from commands2.button import CommandXboxController
from photonlibpy.targeting import PhotonTrackedTarget
from wpilib import DriverStation
from wpilib.interfaces import GenericHID
from wpimath.filter import SlewRateLimiter

from commands.drivetrain.drive import apply_center_distance_deadzone, properties
from modules.algaevision import AlgaeVisionModule
from subsystems.drivetrain import Drivetrain
from ultime.autoproperty import autoproperty
from ultime.command import Command


class AlignWithAlgae(Command):
    p = autoproperty(0.025)
    horizontal_offset = autoproperty(0.0)

    def __init__(
        self,
        drivetrain: Drivetrain,
        vision: AlgaeVisionModule,
        xbox_remote: Optional[CommandXboxController] = None,
    ):
        super().__init__()
        self.addRequirements(drivetrain)
        self.drivetrain = drivetrain
        self.vision = vision
        self.xbox_remote = xbox_remote
        self.hid = xbox_remote.getHID() if xbox_remote else None
        self.vel_rot = 0
        self.target: PhotonTrackedTarget = None
        self.m_xspeedLimiter = SlewRateLimiter(3)
        self.m_yspeedLimiter = SlewRateLimiter(3)

    def execute(self):
        self.target = self.vision.getClosestTarget()

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
