import commands2

from subsystems.arm import Arm
from subsystems.drivetrain import Drivetrain
from ultime.module import Module
from ultime.subsystem import Subsystem


class HardwareModule(Module):
    def __init__(self):
        super().__init__()
        self.drivetrain = Drivetrain()
        self.arm = Arm()

        self.controller = commands2.button.CommandXboxController(0)

        self.subsystems: list[Subsystem] = [self.drivetrain, self.arm]
