from commands2 import Command

from commands.intake.moveintake import MoveIntake
from subsystems.intake import Intake
from ultime.alert import AlertType


class DiagnoseIntake(Command):
    def __init__(self, intake: Intake):
        super().__init__()
        self.addRequirements(intake)
        self.intake = intake

        #self.intake.extend() #TODO
        #self.intake.isRetracted()
        #self.intake.retract()

        self._toExtended_command = MoveIntake.toExtended(self.intake)
        self._toRetract_command = MoveIntake.toRetracted(self.intake)

        self._alert_has_algae_failed = self.intake.createAlert("Intake didn't return correct value in hasAlgae. Is there an actual algae in the robot?", AlertType.Error)
        self._alert_extend_failed = self.intake.createAlert("Intake didn't extend in time. ", AlertType.Error)
        self._alert_is_retracted_failed = self.intake.createAlert("Intake didn't return correct value in isRetracted. Is the sensor properly connected?", AlertType.Error)
        self._alert_retract_failed = self.intake.createAlert("Intake didn't retract in time.", AlertType.Error)

    def initialize(self):


        self._alert_has_algae_failed.set(False)
        self._alert_extend_failed.set(False)
        self._alert_is_retracted_failed.set(False)
        self._alert_retract_failed.set(False)

    def execute(self):
        if self.intake.hasAlgae():
            self._alert_has_algae_failed.set(True)

        if self.intake.state == self.intake.State.Retracted and not self._toExtended_command.isScheduled():
            self._toExtended_command.schedule()

        if self.intake.state == self.intake.State.Extended and not self._toRetract_command.isScheduled():
            self._toRetract_command.schedule()

    def isFinished(self) -> bool:
        return False