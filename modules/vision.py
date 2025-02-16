import wpimath
from wpimath.geometry import Transform3d

from ultime.vision import AbsoluteVision, RelativeVision, VisionMode

### Offset of the camera relative to the middle of the robot. In robot Coordinate system
robot_to_camera_offset = wpimath.geometry.Transform3d(
    wpimath.geometry.Translation3d(0.0, 0.0, 0.0),
    wpimath.geometry.Rotation3d.fromDegrees(0.0, 0.0, 0.0),
)


class VisionModule(AbsoluteVision, RelativeVision):
    def __init__(self):
        super().__init__(
            camera_name="Main Camera", camera_offset=robot_to_camera_offset
        )
        self.mode = VisionMode.Absolute
