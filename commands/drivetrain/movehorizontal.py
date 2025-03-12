from subsystems.drivetrain import Drivetrain
from ultime.autoproperty import autoproperty, FloatProperty, asCallable
from ultime.command import Command


class MoveHorizontal(Command):
    @classmethod
    def right(cls, drivetrain: Drivetrain):
        cmd = cls(drivetrain, lambda: -move_horizontal_properties.speed)
        cmd.setName(MoveHorizontal.__name__ + ".right")
        return cmd

    @classmethod
    def left(cls, drivetrain: Drivetrain):
        cmd = cls(drivetrain, lambda: move_horizontal_properties.speed)
        cmd.setName(MoveHorizontal.__name__ + ".left")
        return cmd

    def __init__(self, drivetrain: Drivetrain, speed: FloatProperty):
        super().__init__()
        self.drivetrain = drivetrain
        self.addRequirements(drivetrain)
        self.speed = asCallable(speed)

    def execute(self):
        self.drivetrain.drive(0, self.speed(), 0, False)

    def end(self, interrupted: bool):
        self.drivetrain.drive(0, 0, 0, True)


class _ClassProperties:
    speed = autoproperty(0.2, subtable=MoveHorizontal.__name__)


move_horizontal_properties = _ClassProperties()
