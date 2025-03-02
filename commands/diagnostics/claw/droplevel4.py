from commands2 import SequentialCommandGroup

from commands.claw.drop import Drop
from subsystems.claw import Claw
from ultime.command import ignore_requirements


@ignore_requirements(["claw"])
class DiagnoseDropLevel4(SequentialCommandGroup):
    def __init__(self, claw: Claw):
        super().__init__(Drop.atLevel4(claw))
        self.claw = claw

    def end(self, interrupted: bool):
        super().end(interrupted)
        if self.claw.has_coral:
            self.claw.alert_drop_failed.set(True)
