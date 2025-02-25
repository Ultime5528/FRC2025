from photonlibpy.targeting import PhotonTrackedTarget

from subsystems.drivetrain import Drivetrain
from ultime.vision import RelativeVision, VisionMode


class AlgaeVisionModule(RelativeVision):
    def __init__(self):
        super().__init__(camera_name="Algae Camera")
        self.mode = VisionMode.Relative

    def getTargetDistance(self, target: PhotonTrackedTarget):
        return target.getPitch()

    def getBestAlgae(self):
        bestAlgae = None
        for target in self._targets:
            if bestAlgae is None or self.getTargetDistance(
                target
            ) < self.getTargetDistance(bestAlgae):
                bestAlgae = target
        return bestAlgae