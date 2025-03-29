import wpimath
from wpimath.geometry import Transform3d

from subsystems.drivetrain import Drivetrain
from ultime.autoproperty import autoproperty
from ultime.timethis import tt
from ultime.vision import AbsoluteVision, VisionMode

### Offset of the camera relative to the middle of the robot. In robot Coordinate system
robot_to_camera_offset = wpimath.geometry.Transform3d(
    wpimath.geometry.Translation3d(0.35, -0.098, 0.236),
    wpimath.geometry.Rotation3d.fromDegrees(0.0, -15.0, 0.0),
)


class TagVisionModule(AbsoluteVision):
    ambiguity_threshold = autoproperty(0.05)

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
        n_used_tags = len(used_tags)

        if n_used_tags > 1 or (
            n_used_tags == 1
            and used_tags[0].getPoseAmbiguity() < self.ambiguity_threshold
        ):
            if estimated_pose is not None:
                time_stamp = self.getEstimatedPoseTimeStamp()
                self.drivetrain.addVisionMeasurement(estimated_pose, time_stamp)

    def getNumberTagsUsed(self) -> int:
        return len(self.getUsedTags())

    def getFirstTagAmbiguity(self) -> float:
        """
        Get the ambiguity of the first tag used, -1.0 if no tag is seen.
        """
        used_tags = self.getUsedTags()

        if used_tags:
            return used_tags[0].getPoseAmbiguity()

        return -1.0

    def initSendable(self, builder):
        super().initSendable(builder)

        def noop(x):
            pass

        builder.addIntegerProperty("number_tags_used", tt(self.getNumberTagsUsed), noop)
        builder.addDoubleProperty(
            "first_tag_ambiguity", tt(self.getFirstTagAmbiguity), noop
        )
        builder.addBooleanProperty(
            "isConnected", self.camera_pose_estimator._camera.isConnected, noop
        )
