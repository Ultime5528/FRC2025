import math

import commands2.button
from wpilib import DriverStation
from wpimath.filter import SlewRateLimiter
from wpimath.geometry import Rotation2d

from subsystems.drivetrain import Drivetrain
from ultime.autoproperty import autoproperty
from ultime.command import Command
from ultime.dynamicmotion import DynamicMotion


def apply_center_distance_deadzone(x_dist, y_dist, deadzone):
    hypot = math.hypot(x_dist, y_dist)
    if hypot <= deadzone:
        return 0.0, 0.0, 0.0
    else:
        return x_dist, y_dist, hypot


def apply_linear_deadzone(_input, deadzone):
    if abs(_input) <= deadzone:
        return 0.0
    else:
        return _input


class DriveField(Command):
    rotation_deadzone = autoproperty(0.3)
    rotate_speed = autoproperty(0.0375)
    rotate_accel = autoproperty(0.01)
    speed_rate = autoproperty(0.33)
    angle_tol = autoproperty(8)

    def __init__(
            self,
            drivetrain: Drivetrain,
            xbox_remote: commands2.button.CommandXboxController,
    ):
        super().__init__()
        self.rot: float = 0.0
        self.actual_rot: Rotation2d = Rotation2d()
        self.addRequirements(drivetrain)
        self.xbox_remote = xbox_remote
        self.drivetrain = drivetrain

    def initialize(self):
        self.rot = self.drivetrain.getPose().rotation()
        self.rot_motion = DynamicMotion(
            goal=0,
            max_speed=self.rotate_speed,
            end_speed=0.00001,
            accel=self.rotate_accel,

        )
        self.rot_motion.update(self.rot.degrees())

    def execute(self):
        x_speed, y_speed, _ = apply_center_distance_deadzone(
            self.xbox_remote.getLeftY() * -1,
            self.xbox_remote.getLeftX() * -1,
            properties.moving_deadzone,
        )

        rot_x, rot_y, rot_hyp = apply_center_distance_deadzone(
            self.xbox_remote.getRightX(),
            -1 * self.xbox_remote.getRightY(),
            self.rotation_deadzone,
        )

        if not (rot_x == 0 and rot_y == 0):
            self.rot = Rotation2d(math.atan2(rot_x, rot_y) * -1)
            if DriverStation.getAlliance() == DriverStation.Alliance.kRed:
                self.rot = Rotation2d.fromDegrees(180 + self.rot.degrees())

        if self.xbox_remote.leftBumper():
            self.actual_rot: Rotation2d = self.rot + Rotation2d.fromDegrees(180.0)
        else:
            self.actual_rot: Rotation2d = self.rot

        rot_speed = self.rot_motion.update((self.drivetrain.getPose().rotation() - self.actual_rot).degrees())
        print((self.actual_rot - self.drivetrain.getPose().rotation()).degrees)
        if DriverStation.getAlliance() == DriverStation.Alliance.kRed:
            x_speed *= -1
            y_speed *= -1

        if self.xbox_remote.rightBumper():
            x_speed *= self.speed_rate
            y_speed *= self.speed_rate

        self.drivetrain.drive(x_speed, y_speed, rot_speed if not self.rot_motion.reachedGoal(self.angle_tol) else 0,
                              True)

    def end(self, interrupted: bool) -> None:
        self.drivetrain.stop()


class _Properties:
    moving_deadzone = autoproperty(0.1, subtable=DriveField.__name__)


properties = _Properties()
