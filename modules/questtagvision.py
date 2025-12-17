import wpimath
from wpimath.geometry import Transform3d, Pose3d

from subsystems.drivetrain import Drivetrain
from ultime.module import Module
from ultime.questnav import questnav
from ultime.timethis import tt

### Offset of the camera relative to the middle of the robot. In robot Coordinate system
robot_to_quest_offset = wpimath.geometry.Transform3d(
    wpimath.geometry.Translation3d(0.20, 0.01, 1.03),
    wpimath.geometry.Rotation3d.fromDegrees(0.0, 0.0, 0.0),
)


class QuestTagVisionModule(Module):

    def __init__(self, drivetrain: Drivetrain):
        super().__init__()
        self.drivetrain = drivetrain
        self.questnav = questnav.QuestNav()
        self.estimated_pose = Pose3d()

    def robotPeriodic(self) -> None:
        super().robotPeriodic()
        poseFrames = self.questnav.getAllUnreadPoseFrames()

        for poseFrame in poseFrames:
            self.estimated_pose = poseFrame.quest_pose_3d
            self.estimated_pose = self.estimated_pose.transformBy(
                robot_to_quest_offset.inverse()
            )
            time_stamp = poseFrame.data_timestamp
            self.drivetrain.addVisionMeasurement(
                self.estimated_pose.toPose2d(),
                time_stamp,
                [0.03, 0.03, 0.1],
            )

    def getX(self):
        return self.estimated_pose.x

    def getY(self):
        return self.estimated_pose.y

    def getZ(self):
        return self.estimated_pose.z

    def getRoll(self):
        return self.estimated_pose.rotation().x

    def getPitch(self):
        return self.estimated_pose.rotation().y

    def getYaw(self):
        return self.estimated_pose.rotation().z

    def reset(self, pose: Pose3d):
        self.questnav.setPose(pose)

    def initSendable(self, builder):
        super().initSendable(builder)

        def noop(x):
            pass

        builder.addFloatProperty("X", tt(self.getX), noop)
        builder.addFloatProperty("Y", tt(self.getY), noop)
        builder.addFloatProperty("Z", tt(self.getZ), noop)
        builder.addFloatProperty("roll", tt(self.getRoll), noop)
        builder.addFloatProperty("pitch", tt(self.getPitch), noop)
        builder.addFloatProperty("yaw", tt(self.getYaw), noop)
