import wpilib
from wpimath.geometry import Pose2d, Rotation2d

from robot import Robot
from subsystems.drivetrain import Drivetrain
from ultime.autoproperty import autoproperty
from ultime.vision import RelativeVision, VisionMode


class AlgaeVisionModule(RelativeVision):
    camera_height = autoproperty(0.236)
    camera_pitch = autoproperty(-15)
    fov = autoproperty(70)
    fov_y = autoproperty(70)
    image_height = autoproperty(320)
    image_width = autoproperty(160)
    def __init__(self, drivetrain: Drivetrain):
        super().__init__(
            camera_name="AlgaeCamera",
            camera_height=self.camera_height,
            camera_pitch=self.camera_pitch,
            fov=self.fov,
            fov_y=self.fov_y,
            image_height=self.image_height,
            image_width=self.image_width,
            drivetrain=drivetrain
        )
        self.mode = VisionMode.Relative
        self._field = wpilib.Field2d()
        wpilib.SmartDashboard.putData("AlgaeField", self._field)

    def robotPeriodic(self) -> None:
        if self.getClosestTargetPose() is not None:
            self._field.setRobotPose(self.getClosestTargetPose())
        else:
            self._field.setRobotPose(Pose2d(0, 0, Rotation2d.fromDegrees(0)))
