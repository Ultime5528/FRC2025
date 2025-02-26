from photonlibpy.targeting import PhotonTrackedTarget

from subsystems.drivetrain import Drivetrain
from ultime.vision import RelativeVision, VisionMode


class RelativeTagVisionModule(RelativeVision):
    def __init__(self):
        super().__init__(camera_name="PositionEstimator")
        self.mode = VisionMode.Relative

    def getTargetDistance(self, target: PhotonTrackedTarget):
        return target.getPitch()

    def getTagFromID(self, id):
        