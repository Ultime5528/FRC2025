import math

import wpimath
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
    distance_meters_to_stop = autoproperty(5.0)
    min_area = autoproperty(10.0)

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
            used_tag = used_tags[0]
            used_tag.getBestCameraToTarget()
            tag_distance = (
                used_tag.getBestCameraToTarget().x ** 2
                + used_tag.getBestCameraToTarget().y ** 2
            )
            tag_area = used_tag.getArea()

            if (
                tag_distance < (self.distance_meters_to_stop**2)
                and tag_area > self.min_area
            ):
                time_stamp = self.getEstimatedPoseTimeStamp()
                self.drivetrain.addVisionMeasurement(estimated_pose, time_stamp)

        elif estimated_pose is not None:
            time_stamp = self.getEstimatedPoseTimeStamp()
            self.drivetrain.addVisionMeasurement(estimated_pose, time_stamp)

    def initSendable(self, builder):
        super().initSendable(builder)

        def noop(x):
            pass

        def getNumberTagUsed() -> int:
            return len(self.getUsedTags())

        def getDistance() -> float:
            if len(self.getUsedTags()) == 1:
                used_tag = self.getUsedTags()[0]
                return math.sqrt(
                    used_tag.getBestCameraToTarget().x ** 2
                    + used_tag.getBestCameraToTarget().y ** 2
                )
            else:
                return 0.0

        def getArea() -> float:
            if len(self.getUsedTags()) == 1:
                used_tag = self.getUsedTags()[0]
                return used_tag.getArea()
            else:
                return 0.0

        builder.addIntegerProperty("NumberOfTagUsed", getNumberTagUsed, noop)
        builder.addFloatProperty("DistanceOfTheTag", getDistance, noop)
        builder.addFloatProperty("AreaOfTheTag", getArea, noop)
