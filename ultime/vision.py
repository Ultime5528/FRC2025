from enum import Enum, auto
from typing import List
from typing import Optional

from photonlibpy import PhotonPoseEstimator, PoseStrategy, EstimatedRobotPose
from photonlibpy.photonCamera import PhotonCamera
from photonlibpy.targeting import PhotonTrackedTarget
from robotpy_apriltag import AprilTagFieldLayout, AprilTagField
from wpimath.geometry import Transform3d

from ultime.module import Module


class VisionMode(Enum):
    Relative = auto()
    Absolute = auto()


class Vision(Module):
    def __init__(self, camera_name: str):
        super().__init__()
        self.camera_name = camera_name
        self._cam = PhotonCamera(self.camera_name)
        self.mode = VisionMode.Relative


class RelativeVision(Vision):
    def __init__(self, camera_name: str):
        super().__init__(camera_name=camera_name)

        self._targets: List[PhotonTrackedTarget] = []

    def robotPeriodic(self) -> None:
        super().robotPeriodic()

        if self.mode == VisionMode.Relative:
            if self._cam.isConnected():
                self._targets = self._cam.getLatestResult().getTargets()
            else:
                self._targets = []

    def getTargetWithID(self, _id: int) -> Optional[PhotonTrackedTarget]:
        for target in self._targets:
            if target.getFiducialId() == _id:
                return target
        return None


class AbsoluteVision(Vision):
    def __init__(self, camera_name: str, camera_offset: Transform3d):
        super().__init__(camera_name=camera_name)

        self.camera_pose_estimator = PhotonPoseEstimator(
            AprilTagFieldLayout.loadField(AprilTagField.kDefaultField),
            PoseStrategy.MULTI_TAG_PNP_ON_COPROCESSOR,
            self._cam,
            camera_offset,
        )
        self.estimated_pose: EstimatedRobotPose = None
        self.camera_pose_estimator.multiTagFallbackStrategy = (
            PoseStrategy.LOWEST_AMBIGUITY
        )

    def robotPeriodic(self) -> None:
        super().robotPeriodic()

        if self.mode == VisionMode.Absolute:
            self.estimated_pose = self.camera_pose_estimator.update()

    def getEstimatedPose3D(self):
        if self.estimated_pose:
            return self.estimated_pose.estimatedPose
        else:
            return None

    def getEstimatedPose2D(self):
        if self.estimated_pose:
            return self.estimated_pose.estimatedPose.toPose2d()
        else:
            return None

    def getEstimatedPoseTimeStamp(self):
        if self.estimated_pose:
            return self.estimated_pose.timestampSeconds

    def getUsedTagIDs(self) -> list[int]:
        if self.estimated_pose:
            return [target.fiducialId for target in self.estimated_pose.targetsUsed]
        else:
            return []

    def getUsedTags(self) -> list[PhotonTrackedTarget]:
        if self.estimated_pose:
            return self.estimated_pose.targetsUsed
        else:
            return []

    def initSendable(self, builder):
        super().initSendable(builder)

        def noop(x):
            pass

        builder.addIntegerArrayProperty("UsedTagIDs", self.getUsedTagIDs, noop)
