from commands2 import Command
from subsystems.intake import Intake


class DiagnoseHasAlgae(Command):
    def __init__(self, intake: Intake):
        super().__init__()
        self.addRequirements(intake)
        self.intake = intake

    def initialize(self):
        if self.intake.hasAlgae():
            self.intake.alert_has_algae_failed.set(True)
        else:
            self.intake.alert_has_algae_failed.set(False)

    def isFinished(self) -> bool:
        return True
