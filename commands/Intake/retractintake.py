from commands2 import Command

from subsystems.intake import Intake


class RetractIntake(Command):
    def __init__(self, intake: Intake):
        super().__init__()
        self.intake = intake
        self.switch = self.intake.pivot_switch

    def execute(self):
        self.intake.retractPivot()

    def isFinished(self) -> bool:
        return self.intake.pivot_switch.isPressed()

    def end(self, interrupted: bool):
        self.intake.stopPivot()
