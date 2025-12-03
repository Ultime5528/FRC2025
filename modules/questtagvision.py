import wpimath
from wpimath.geometry import Transform3d, Rotation3d, Pose3d, Translation3d

from subsystems.drivetrain import Drivetrain
from ultime.autoproperty import autoproperty
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

        # Documentation of get_all_unread_pose_frames uses all poseFrames
        # Here we choose to use only the last one.... should we???
        if len(poseFrames) > 0:
            poseFrame = poseFrames[-1]
            self.estimated_pose = poseFrame.quest_pose_3d
            self.estimated_pose = self.estimated_pose.transformBy(robot_to_quest_offset.inverse())
            time_stamp = poseFrame.data_timestamp
            self.drivetrain.addVisionMeasurement(self.estimated_pose.toPose2d(), time_stamp)

    def X(self):
        return self.estimated_pose.X()

    def Y(self):
        return self.estimated_pose.Y()

    def Z(self):
        return self.estimated_pose.Z()

    def Roll(self):
        return self.estimated_pose.rotation().X()

    def Pitch(self):
        return self.estimated_pose.rotation().Y()

    def Yaw(self):
        return self.estimated_pose.rotation().Z()

    def initSendable(self, builder):
        super().initSendable(builder)

        def noop(x):
            pass

        builder.addFloatProperty("X", tt(self.X), noop)
        builder.addFloatProperty("Y", tt(self.Y), noop)
        builder.addFloatProperty("Z", tt(self.Z), noop)
        builder.addFloatProperty("roll", tt(self.Roll), noop)
        builder.addFloatProperty("pitch", tt(self.Pitch), noop)
        builder.addFloatProperty("yaw", tt(self.Yaw), noop)
