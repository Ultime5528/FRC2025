from subsystems.Vision.vision import Vision


class VisionPoseEstimator(Vision):
    def __init__(self):
        super().__init__(cameraname="PoseCamera")

    def getEstimatedPose3D(self):
        return self.multi_tag_result.estimatedPose

    def getEstimatedPose2D(self):
        pose = self.multi_tag_result.estimatedPose
        if pose is not None:
            return pose
        return None

    def getUsedTagID(self):
        return self.multi_tag_result.fiducialIDsUsed

    def initSendable(self, builder):
        def noop(x):
            pass

        def getUsedTag():
            if self.getUsedTagID() is not None:
                return self.getUsedTagID()
            return 0

        def getEstimatedPose():
            if self.getEstimatedPose2D() is not None:
                return self.getEstimatedPose2D()
            return 0.0

        builder.addIntegerArrayProperty("Used_Tags", getUsedTag(), noop)
        builder.addFloatProperty("Estimated_pose_2D", getEstimatedPose(), noop)
