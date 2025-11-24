import wpimath
from wpimath.geometry import Transform3d, Rotation3d, Pose3d, Translation3d

from subsystems.drivetrain import Drivetrain
from ultime.autoproperty import autoproperty
from ultime.module import Module
from ultime.timethis import tt
from ultime.questnav.questnav import QuestNav

### Offset of the camera relative to the middle of the robot. In robot Coordinate system
robot_to_camera_offset = wpimath.geometry.Transform3d(
    wpimath.geometry.Translation3d(0.35, -0.098, 0.236),
    wpimath.geometry.Rotation3d.fromDegrees(0.0, -15.0, 0.0),
)


class QuestTagVisionModule(Module):
    ambiguity_threshold = autoproperty(0.05)

    def __init__(self, drivetrain: Drivetrain):
        super().__init__()
        self.drivetrain = drivetrain
        self.questnav = QuestNav()
        self.estimated_pose = Pose3d(1,2,3,Rotation3d(4,5,6))


    def robotPeriodic(self) -> None:
        super().robotPeriodic()
        #self.estimated_pose = self.questnav.get_pose3d()
        self.estimated_pose = Pose3d(Translation3d(), Rotation3d())


        time_stamp = self.questnav.get_data_timestamp()
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
