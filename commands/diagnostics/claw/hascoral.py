from commands2 import Command

from subsystems.claw import Claw


class DiagnoseHasCoral(Command):
    def __init__(self, claw: Claw):
        super().__init__()
        self.addRequirements(claw)
        self.claw = claw

    def initialize(self):
        if not self.claw.seesObject():
            self.claw.alert_has_coral.set(True)

    def isFinished(self) -> bool:
        return self.claw.seesObject()
