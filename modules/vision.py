from photonlibpy import PhotonPoseEstimator, PoseStrategy
from robotpy_apriltag import AprilTagFieldLayout, AprilTagField
from wpimath.geometry import Transform3d

from ultime.vision import Vision


class VisionModule(Vision):
    def __init__(self, cameraname: str, camera_offset: Transform3d):
        super().__init__(
            cameraname=cameraname
        )
        self.camera_pose_estimator = PhotonPoseEstimator(
            AprilTagFieldLayout.loadField(AprilTagField.kDefaultField),
            PoseStrategy.MULTI_TAG_PNP_ON_COPROCESSOR,
            self._cam,
            camera_offset,
        )



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

    def getUsedTagIDs(self):
        if self.estimated_pose:
            return [target.fiducialId for target in self.estimated_pose.targetsUsed]
        else:
            return []

    def initSendable(self, builder):
        def noop(x):
            pass

        builder.addIntegerArrayProperty("UsedTagIDs", self.getUsedTagIDs, noop)
        # builder.add("Estimated_pose_2D", self.getEstimatedPose2D, noop)
