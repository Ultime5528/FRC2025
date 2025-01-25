import commands2

from subsystems.drivetrain import Drivetrain
from subsystems.Vision.visionposeestimator import VisionPoseEstimator
from ultime.module import Module
from commands.drivetrain.drive import DriveField


class HardwareModule(Module):
    def __init__(self):
        super().__init__()
        self.drivetrain = Drivetrain(0.02)
        self.vision_pose_estimator = VisionPoseEstimator()
        self.controller = commands2.button.CommandXboxController(0)
        self.drivetrain.setDefaultCommand(DriveField(self.drivetrain, self.controller))
