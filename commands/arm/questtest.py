from commands2 import Command

from ultime.questnav.questnav import QuestNav


class QuestTest(Command):

    def __init__(self):
        super().__init__()
        self.questnav = QuestNav()

    def initialize(self):
        pass

    def execute(self):
        print(
            self.questnav.is_connected(),
            self.questnav.get_battery_percent(),
            self.questnav.is_tracking(),
            self.questnav.get_pose3d(),
        )

    def isFinished(self) -> bool:
        pass

    def end(self, interrupted: bool):
        pass
