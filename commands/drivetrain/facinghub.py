import wpilib
import math

from wpimath.units import shots

from subsystems.drivetrain import Drivetrain
from wpimath.geometry import Pose2d
from wpimath.geometry import Transform2d

from commands2 import Command

shooter_offset1 = Pose2d(0.4,0.4,math.pi*3/4)

def facing_hub(robot_pose2d: Pose2d, shooter_offset: Pose2d, hubpose: Pose2d):
    shooter_pose = shooter_offset.transformBy(Transform2d(robot_pose2d, robot_pose2d))
    shooter_to_pose = shooter_pose.relativeTo(hubpose)
    robot_to_pose = robot_pose2d.relativeTo(hubpose)

    return shooter_to_pose,robot_to_pose

class AlignWithHub(Command):
    def __init__(self, drivetrain: Drivetrain):
        super().__init__()
        self.drivetrain = drivetrain
        self.addRequirements(drivetrain)

    def initialize(self):
        facing_hub(self.drivetrain.getPose(),shooter_offset1,Pose2d(5,5,0))

    def end(self, interrupted: bool):
        self.drivetrain.resetGyro()







