from commands2 import Command

from ultime.questnav.questnav import QuestNav
from wpimath.geometry import Pose3d, Translation3d, Rotation3d


class QuestTest(Command):

    def __init__(self):
        super().__init__()
        self.questnav = QuestNav()

    def initialize(self):
        self.questnav.set_3dpose(Pose3d(100,100,100,Rotation3d(100,100,100)))

    def execute(self):
        pass

    def isFinished(self) -> bool:
        return True

    def end(self, interrupted: bool):
        pass
