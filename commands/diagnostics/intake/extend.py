from commands2 import SequentialCommandGroup

from commands.intake.moveintake import MoveIntake
from commands.intake.resetintake import ResetIntake
from subsystems.intake import Intake
from ultime.command import ignore_requirements


@ignore_requirements(["intake"])
class DiagnoseExtend(SequentialCommandGroup):
    def __init__(self, intake: Intake):
        super().__init__(ResetIntake(intake), MoveIntake.toExtended(intake))

        self.intake = intake

    def end(self, interrupted: bool):
        super().end(interrupted)
        if self.intake.isRetracted() or self.intake.state != Intake.State.Extended:
            self.intake.alert_extend_failed.set(True)

            if self.intake.isRetracted() and self.intake.state == Intake.State.Extended:
                self.intake.alert_is_retracted_failed.set(True)
