from commands2 import Command

from subsystems.intake import Intake


class ExtendIntake(Command):
    def __init__(self, intake: Intake):
        super().__init__()

        self.intake = intake

    def execute(self):
        self.intake.extendPivot()

    def isFinished(self) -> bool:
        return self.intake.pivot_encoder.get() >= self.intake.pivot_encoder_threshold

    def end(self, interrupted: bool):
        self.intake.stopPivot()
