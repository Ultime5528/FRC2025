import wpilib
from wpimath.geometry import Pose2d, Rotation2d

from ultime.vision import RelativeVision, VisionMode


class AlgaeVisionModule(RelativeVision):
    def __init__(self):
        super().__init__(
            camera_name="AlgaeCamera",
            camera_height=0.236,
            camera_pitch=-15,
            fov=70,
            fov_y=70,
            image_height=320,
            image_width=160,
        )
        self.mode = VisionMode.Relative
        self._field = wpilib.Field2d()
        wpilib.SmartDashboard.putData("AlgaeField", self._field)

    def robotPeriodic(self) -> None:
        if self.getClosestTargetPose() is not None:
            self._field.setRobotPose(self.getClosestTargetPose())
        else:
            self._field.setRobotPose(Pose2d(0, 0, Rotation2d.fromDegrees(0)))
