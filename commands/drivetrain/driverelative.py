from wpimath.geometry import Translation2d

from subsystems.drivetrain import Drivetrain
from ultime.autoproperty import autoproperty, FloatProperty, asCallable
from ultime.command import Command


class DriveRelative(Command):

    @classmethod
    def right(cls, drivetrain: Drivetrain):
        cmd = cls(drivetrain, Translation2d(0, -1), drive_relative_properties.speed)
        cmd.setName(DriveRelative.__name__ + ".right")
        return cmd

    @classmethod
    def left(cls, drivetrain: Drivetrain):
        cmd = cls(drivetrain, Translation2d(0, 1), drive_relative_properties.speed)
        cmd.setName(DriveRelative.__name__ + ".left")
        return cmd

    @classmethod
    def forwards(cls, drivetrain: Drivetrain):
        cmd = cls(drivetrain, Translation2d(1, 0), drive_relative_properties.speed)
        cmd.setName(DriveRelative.__name__ + ".forwards")
        return cmd

    @classmethod
    def backwards(cls, drivetrain: Drivetrain):
        cmd = cls(drivetrain, Translation2d(-1, 0), drive_relative_properties.speed)
        cmd.setName(DriveRelative.__name__ + ".backwards")
        return cmd

    def __init__(
        self, drivetrain: Drivetrain, direction: Translation2d, speed: FloatProperty
    ):
        super().__init__()
        self.drivetrain = drivetrain
        self.addRequirements(drivetrain)
        self.direction = direction
        self.normalized_speed = Translation2d()
        self.speed = asCallable(speed)

    def initialize(self):
        self.normalized_speed = self.direction / self.direction.norm() * self.speed()

    def execute(self):
        self.drivetrain.drive(
            self.normalized_speed.x, self.normalized_speed.y, 0, False
        )

    def end(self, interrupted: bool):
        self.drivetrain.stop()


class _ClassProperties:
    speed = autoproperty(0.2, subtable=DriveRelative.__name__)


drive_relative_properties = _ClassProperties()
