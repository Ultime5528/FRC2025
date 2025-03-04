from commands2 import Command

from ultime.subsystem import Subsystem


class SetRunningTest(Command):
    def __init__(self, subsystem: Subsystem, is_running_test: bool):
        super().__init__()
        self.subsystem = subsystem
        self.is_running_test = is_running_test

    def initialize(self):
        self.subsystem.running_test.set(self.is_running_test)

    def isFinished(self) -> bool:
        return True
