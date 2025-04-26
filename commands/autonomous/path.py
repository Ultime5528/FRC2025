import choreo
import wpilib
from choreo import SwerveTrajectory

from modules.hardware import HardwareModule
from ultime.command import Command

class Path(Command):
    def __init__(self, hardware: HardwareModule):
        super().__init__()
        try:
            self.trajectory = choreo.load_swerve_trajectory("path\Testfield")
        except ValueError:
            self.trajectory = None

        self.drivetrain = hardware.drivetrain
        self.timer = wpilib.Timer()

    def initialize(self):
        self.timer.restart()
        self.last_choreo_timestamp = -1.0

    def execute(self):
        if self.trajectory:
            sample = self.trajectory.sample_at(self.timer.get(), self.is_red_alliance())

            if sample and sample.timestamp != self.last_choreo_timestamp:
                print(sample.fx)
                self.last_choreo_timestamp = sample.timestamp
                self.drivetrain.followTrajecctory(sample)

    def is_red_alliance(self):
        return wpilib.DriverStation.getAlliance() == wpilib.DriverStation.Alliance.kRed
