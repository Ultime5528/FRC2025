import commands2

from subsystems.drivetrain import Drivetrain
from ultime.module import Module
from ultime.subsystem import Subsystem


class HardwareModule(Module):
    def __init__(self):
        super().__init__()
        self.drivetrain = Drivetrain()
        self.controller = commands2.button.CommandXboxController(0)

        self.subsystems: list[Subsystem] = [self.drivetrain, self.controller]
