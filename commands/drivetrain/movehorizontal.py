from subsystems.drivetrain import Drivetrain
from ultime.command import Command

class MoveHorizontal(Command):
    @classmethod
    def moveRight(cls, drivetrain: Drivetrain):
        cmd = MoveHorizontal(drivetrain, -0.2)
        return cmd

    def __init__(self, drivetrain: Drivetrain, speed: float):
        super().__init__()
        self.drivetrain = drivetrain
        self.speed = speed

    def execute(self):
        self.drivetrain.drive(self.speed, 0, 0, False)

    def end(self, interrupted: bool):
        self.drivetrain.drive(0, 0, 0, True)