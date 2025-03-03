import wpimath
from wpilib import SmartDashboard
from wpimath.geometry import Transform3d

from subsystems.drivetrain import Drivetrain
from ultime.autoproperty import autoproperty
from ultime.vision import AbsoluteVision, VisionMode

### Offset of the camera relative to the middle of the robot. In robot Coordinate system
robot_to_camera_offset = wpimath.geometry.Transform3d(
    wpimath.geometry.Translation3d(0.35, -0.098, 0.236),
    wpimath.geometry.Rotation3d.fromDegrees(0.0, -15.0, 0.0),
)


class TagVisionModule(AbsoluteVision):
    ambiguity_threshold = autoproperty(0.2)

    def __init__(self, drivetrain: Drivetrain):
        super().__init__(
            camera_name="PositionEstimator", camera_offset=robot_to_camera_offset
        )
        self.mode = VisionMode.Absolute
        self.drivetrain = drivetrain

    def robotPeriodic(self) -> None:
        super().robotPeriodic()
        estimated_pose = self.getEstimatedPose2D()
        used_tags = self.getUsedTags()

        if len(used_tags) == 1:
            if used_tags[0].getPoseAmbiguity() < self.ambiguity_threshold:
                time_stamp = self.getEstimatedPoseTimeStamp()
                self.drivetrain.addVisionMeasurement(estimated_pose, time_stamp)

        elif estimated_pose is not None:
            time_stamp = self.getEstimatedPoseTimeStamp()
            self.drivetrain.addVisionMeasurement(estimated_pose, time_stamp)

        SmartDashboard.putNumber("NumberOfTagUsed", self.getNumberTagUsed())
        SmartDashboard.putNumber("AmbiguityOfTheTag", self.getAmbiguity())

    def getNumberTagUsed(self) -> int:
        return len(self.getUsedTags())

    def getAmbiguity(self) -> float:
        if len(self.getUsedTags()) == 1:
            return self.getUsedTags()[0].getPoseAmbiguity()
        return 5528

    # def initSendable(self, builder):
    #     super().initSendable(builder)
    #
    #     def noop(x):
    #         pass
    #
