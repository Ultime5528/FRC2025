from commands2 import Command

from ultime.command import ignore_requirements
from ultime.subsystem import Subsystem


@ignore_requirements(["subsystem"])
class SetRunningTest(Command):
    def __init__(self, subsystem: Subsystem, is_running_test: bool):
        super().__init__()
        self.subsystem = subsystem
        self.is_running_test = is_running_test

    def initialize(self):
        self.subsystem.running_test.set(self.is_running_test)

    def isFinished(self) -> bool:
        return True
