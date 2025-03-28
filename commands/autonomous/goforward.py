from commands2 import SequentialCommandGroup

from commands.drivetrain.driverelative import DriveRelative
from commands.resetautonomous import ResetAutonomous
from modules.hardware import HardwareModule


class GoForwardAuto(SequentialCommandGroup):
    def __init__(self, hardware: HardwareModule):
        super().__init__()
        driv = hardware.drivetrain

        self.addCommands(
            ResetAutonomous(hardware.elevator, hardware.printer, hardware.arm),
            DriveRelative.forwards(driv).withTimeout(2.0),
        )
