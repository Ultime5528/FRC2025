from commands2 import SequentialCommandGroup

from commands.claw.loadcoral import LoadCoral
from subsystems.claw import Claw


class DiagnoseDropLevel4(SequentialCommandGroup):
    def __init__(self, claw: Claw):
        self.addRequirements(claw)
        self.claw = claw

        super().__init__(LoadCoral(claw))

    def end(self, interrupted: bool):
        super().end(interrupted)
        if self.claw.has_coral:
            self.claw.alert_drop_failed.set(True)
