import math
from enum import Enum, auto
from typing import List
from typing import Optional

from photonlibpy import PhotonPoseEstimator, PoseStrategy, EstimatedRobotPose
from photonlibpy.photonCamera import PhotonCamera
from photonlibpy.targeting import PhotonTrackedTarget
from robotpy_apriltag import AprilTagFieldLayout, AprilTagField
from wpimath.geometry import Transform3d, Pose2d, Rotation2d

from ultime.alert import AlertType
from ultime.module import Module
from ultime.timethis import tt

april_tag_field_layout = AprilTagFieldLayout.loadField(
    AprilTagField.k2025ReefscapeWelded
)


class VisionMode(Enum):
    Relative = auto()
    Absolute = auto()


class Vision(Module):
    def __init__(self, camera_name: str):
        super().__init__()
        self.camera_name = camera_name
        self._cam = PhotonCamera(self.camera_name)
        self.mode = VisionMode.Relative

        self.alert_vision_offline = self.createAlert(
            "Vision camera is having connection issues, check for connections?",
            AlertType.Error,
        )

    def robotPeriodic(self) -> None:
        self.alert_vision_offline.set(not self._cam.isConnected())


class RelativeVision(Vision):
    def __init__(
        self,
        camera_name: str,
        camera_height: float,
        camera_pitch: float,
        fov: float,
        fov_y: float,
        image_height: float,
        image_width: float,
    ):
        super().__init__(camera_name=camera_name)
        self._targets: List[PhotonTrackedTarget] = []
        self.camera_height = camera_height
        self.camera_pitch = camera_pitch
        self.fov = fov
        self.fov_y = fov_y
        self.image_height = image_height
        self.image_width = image_width

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

    def getClosestTarget(self):
        bestTarget = None
        for target in self._targets:
            if bestTarget is None or target.getPitch() < bestTarget.getPitch():
                bestTarget = target
        return bestTarget

    def getClosestTargetPose(self) -> Optional[Pose2d]:
        target = self.getClosestTarget()

        if target is not None:
            target_yaw = (
                (target.getYaw() - self.image_width / 2) / (self.image_width / 2)
            ) * (self.fov / 2)
            target_pitch = (
                (self.image_height / 2 - target.pitch) / (self.image_height / 2)
            ) * (self.fov_y / 2)

            dx = math.cos(target_pitch) * math.cos(target_yaw)
            dy = math.cos(target_pitch) * math.sin(target_yaw)
            dz = math.sin(target_pitch)

            dz_cam = math.sin(self.camera_pitch)
            dz_world = dz * math.cos(self.camera_pitch) - dz * dz_cam

            t = -self.camera_height / dz_world

            X = t * dx
            Y = t * dy
            return Pose2d(X, Y, Rotation2d.fromDegrees(0))
        return None


class AbsoluteVision(Vision):
    def __init__(self, camera_name: str, camera_offset: Transform3d):
        super().__init__(camera_name=camera_name)

        self.camera_pose_estimator = PhotonPoseEstimator(
            april_tag_field_layout,
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

        builder.addIntegerArrayProperty("UsedTagIDs", tt(self.getUsedTagIDs), noop)
