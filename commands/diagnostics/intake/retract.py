from commands2 import SequentialCommandGroup

from commands.intake.moveintake import MoveIntake
from commands.intake.resetintake import ResetIntake
from subsystems.intake import Intake
from ultime.command import ignore_requirements


@ignore_requirements(["intake"])
class DiagnoseRetract(SequentialCommandGroup):
    def __init__(self, intake: Intake):
        super().__init__(ResetIntake(intake), MoveIntake.toRetracted(intake))
        self.intake = intake

    def end(self, interrupted: bool):
        super().end(interrupted)
        if not self.intake.isRetracted() or self.intake.state != Intake.State.Retracted:
            self.intake.alert_retract_failed.set(True)

            if (
                not self.intake.isRetracted()
                and self.intake.state == Intake.State.Retracted
            ):
                self.intake.alert_is_retracted_failed.set(True)
