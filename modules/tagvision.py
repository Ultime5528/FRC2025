import wpimath
from wpimath.geometry import Transform3d
from subsystems.drivetrain import Drivetrain
from ultime.vision import AbsoluteVision, RelativeVision, VisionMode

### Offset of the camera relative to the middle of the robot. In robot Coordinate system
robot_to_camera_offset = wpimath.geometry.Transform3d(
    wpimath.geometry.Translation3d(0.0, 0.0, 0.0),
    wpimath.geometry.Rotation3d.fromDegrees(0.0, 0.0, 0.0),
)


class TagVisionModule(AbsoluteVision):
    def __init__(self, drivetrain: Drivetrain):
        super().__init__(
            camera_name="Main Camera", camera_offset=robot_to_camera_offset
        )
        self.mode = VisionMode.Absolute
        self.drivetrain = drivetrain

    def robotPeriodic(self) -> None:
        super().robotPeriodic()
        estimated_pose = self.getEstimatedPose3D()
        if estimated_pose is not None:
            time_stamp = self.getEstimatedPoseTimeStamp()
            self.drivetrain.addVisionMeasurement(estimated_pose, time_stamp)
