from wpimath.geometry import Transform3d
import wpimath

from ultime.vision import AbsoluteVision, RelativeVision, VisionMode

### Offset of the camera relative to the middle of the robot. In robot Coordinate system
camera_offset_to_robot = wpimath.geometry.Transform3d(
    wpimath.geometry.Translation3d(0.0, 0.0, 0.0),
    wpimath.geometry.Rotation3d.fromDegrees(0.0, 0.0, 0.0),
)

class VisionModule(AbsoluteVision, RelativeVision):
    def __init__(self):
        super().__init__(camera_name="Main Camera", camera_offset=camera_offset_to_robot)
        self.mode = VisionMode.Absolute

    def getEstimatedPose(self):
        return self.getEstimatedPose2D()

    def getEstimatedPoseTimeStamp(self):
        return self.getTimeStamp()
