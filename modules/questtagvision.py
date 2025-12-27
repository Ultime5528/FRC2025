import wpimath
from wpimath.geometry import Transform3d, Pose3d

from subsystems.drivetrain import Drivetrain
from ultime.module import Module
from ultime.questnav import questnav
from ultime.timethis import tt

### Offset of the camera relative to the middle of the robot. In robot Coordinate system
robot_to_quest_offset = wpimath.geometry.Transform3d(
    wpimath.geometry.Translation3d(0.20, 0.001, 1.03),
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
        poseFrames = self.questnav.get_all_unread_pose_frames()

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

    def get_X(self):
        return self.estimated_pose.x

    def get_Y(self):
        return self.estimated_pose.y

    def get_Z(self):
        return self.estimated_pose.z

    def get_Roll(self):
        return self.estimated_pose.rotation().x

    def get_Pitch(self):
        return self.estimated_pose.rotation().y

    def get_Yaw(self):
        return self.estimated_pose.rotation().z

    def reset(self, pose: Pose3d):
        self.questnav.set_pose(pose)

    def initSendable(self, builder):
        super().initSendable(builder)

        def noop(x):
            pass

        builder.addFloatProperty("X", tt(self.get_X), noop)
        builder.addFloatProperty("Y", tt(self.get_Y), noop)
        builder.addFloatProperty("Z", tt(self.get_Z), noop)
        builder.addFloatProperty("roll", tt(self.get_Roll), noop)
        builder.addFloatProperty("pitch", tt(self.get_Pitch), noop)
        builder.addFloatProperty("yaw", tt(self.get_Yaw), noop)