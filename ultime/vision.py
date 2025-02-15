from typing import List

from photonlibpy import PhotonPoseEstimator, PoseStrategy, EstimatedRobotPose
from photonlibpy.photonCamera import PhotonCamera
from photonlibpy.targeting import PhotonTrackedTarget
from robotpy_apriltag import AprilTagFieldLayout, AprilTagField
from wpimath.geometry import Transform3d
from wpiutil import Sendable
from ultime.module import Module

class Vision(Module):
    def __init__(self, camera_name: str):
        super().__init__()
        self.camera_name = camera_name
        self._cam = PhotonCamera(self.camera_name)


class RelativeVision(Vision):
    pass

class AbsoluteVision(Vision):
    pass