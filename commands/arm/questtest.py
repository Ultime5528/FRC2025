from commands2 import Command
from wpimath.geometry import Pose3d, Rotation3d

from ultime.questnav.questnav import QuestNav


class QuestTest(Command):

    def __init__(self):
        super().__init__()
        self.questnav = QuestNav()

    def initialize(self):
        self.questnav.set_pose(Pose3d(0, 0, 0, Rotation3d(0, 0, 0)))

    def execute(self):
        pass

    def isFinished(self) -> bool:
        return True

    def end(self, interrupted: bool):
        pass
