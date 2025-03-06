from commands2 import Command

from subsystems.claw import Claw
from ultime.command import ignore_requirements


@ignore_requirements(["claw"])
class WaitUntilCoral(Command):

    def __init__(self, claw: Claw):
        super().__init__()
        self.claw = claw

    def isFinished(self) -> bool:
        return self.claw.seesObject()
