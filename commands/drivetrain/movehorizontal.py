from subsystems.drivetrain import Drivetrain
from ultime.command import Command


class MoveHorizontal(Command):
    @classmethod
    def right(cls, drivetrain: Drivetrain):
        cmd = cls(drivetrain, -0.2)
        cmd.setName(MoveHorizontal.__name__ + ".right")
        return cmd

    @classmethod
    def left(cls, drivetrain: Drivetrain):
        cmd = cls(drivetrain, 0.2)
        cmd.setName(MoveHorizontal.__name__ + ".left")
        return cmd

    def __init__(self, drivetrain: Drivetrain, speed: float):
        super().__init__()
        self.drivetrain = drivetrain
        self.addRequirements(drivetrain)
        self.speed = speed

    def execute(self):
        self.drivetrain.drive(0, self.speed, 0, False)

    def end(self, interrupted: bool):
        self.drivetrain.drive(0, 0, 0, True)
