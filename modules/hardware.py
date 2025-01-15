import commands2

from subsystems.drivetrain import Drivetrain
from ultime.module import Module


class HardwareModule(Module):
    def __init__(self):
        super().__init__()
        self.drivetrain = Drivetrain(0.02)
        self.controller = commands2.button.CommandXboxController(0)
