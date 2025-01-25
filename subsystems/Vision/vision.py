from typing import List

from photonlibpy.photonCamera import PhotonCamera
from photonlibpy.targeting import PhotonTrackedTarget, MultiTargetPNPResult
from wpimath.geometry import Pose3d
from wpiutil import Sendable


class Vision(Sendable):
    def __init__(self, cameraname: str):
        super().__init__()
        self.cameraName = cameraname
        self._cam = PhotonCamera(self.cameraName)
        self._targets: List[PhotonTrackedTarget] = []
        self.multi_tag_result: MultiTargetPNPResult = None

    def periodic(self):
        if self._cam.isConnected():
            self._targets = self._cam.getLatestResult().getTargets()
            self.multi_tag_result = self._cam.getLatestResult().multitagResult
        else:
            self.multi_tag_result = None
            self._targets = []
