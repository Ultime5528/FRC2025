from commands2 import SequentialCommandGroup

from commands.intake.moveintake import MoveIntake
from commands.intake.resetintake import ResetIntake
from subsystems.intake import Intake


class DiagnoseRetract(SequentialCommandGroup):
    def __init__(self, intake: Intake):
        self.addRequirements(intake)
        self.intake = intake

        super().__init__(
            ResetIntake(self.intake),
            MoveIntake.toRetracted(self.intake)
        )

    def end(self, interrupted: bool):
        super().end(interrupted)
        if self.intake.isRetracted() and self.intake.state == Intake.State.Retracted:
            self.intake.alert_retract_failed.set(False)
        else:
            if not self.intake.isRetracted() and self.intake.state == Intake.State.Retracted:
                self.intake.alert_is_retracted_failed.set(True)
            else:
                self.intake.alert_retract_failed.set(True)

