import math

from wpimath._controls._controls.trajectory import TrajectoryConfig
from wpimath.geometry import Pose2d, Rotation2d

from commands.drivetrain.drivetoposes import DriveToPoses
from subsystems.drivetrain import Drivetrain
from ultime.command import DeferredCommand, Command
from ultime.pathfinder import Pathfinder, Obstacle, ObstacleType


class PathFinding(DeferredCommand):
    def __init__(self, drivetrain: Drivetrain):
        super().__init__()
        self.drivetrain = drivetrain
        self.addRequirements(drivetrain)
        self.reef_blue = Obstacle(ObstacleType.HEXAGON, (4.56, 4.03, 2.3749/2, math.pi/6))
        self.reef_red = Obstacle(ObstacleType.HEXAGON, (13.04, 4.03, 2.3749/2, math.pi/6))

    def createCommand(self) -> Command:
        return DriveToPoses(self.drivetrain, self.getPath())

    def getPath(self) -> list[Pose2d]:
        pathfinder = Pathfinder(self.drivetrain.getPose(), Pose2d(15, 4.03, Rotation2d.fromDegrees(75)))
        pathfinder.add_obstacle(self.reef_blue)
        pathfinder.add_obstacle(self.reef_red)
        path = pathfinder.find_path()
        pathfinder.visualize_path(path)
        return path