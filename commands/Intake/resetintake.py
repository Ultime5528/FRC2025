from commands2 import Command

from subsystems.intake import Intake


class ResetIntake(Command):
    def __init__(self, intake: Intake):
        super().__init__()
        self.intake = intake
        self.addRequirements(intake)
        self.pivot_switch_was_pressed = False

    def initialize(self):
        self.pivot_switch_was_pressed = False
        self.intake.state = self.intake.State.Moving

    def execute(self):
        if self.intake.isRetracted():  # If the pivot switch is pressed extend.
            self.intake.extendPivot()
            self.pivot_switch_was_pressed = True
        else:
            self.intake.retractPivot()  # if pivot switch is not pressed retract until pressed.

    def isFinished(self) -> bool:
        return not self.intake.isRetracted() and self.pivot_switch_was_pressed

    def end(self, interrupted: bool):
        self.intake.state = self.intake.State.Reset
        self.intake.stopPivot()
