from commands2 import SequentialCommandGroup

from commands.claw.drop import Drop
from subsystems.claw import Claw


class DiagnoseLoad(SequentialCommandGroup):
    def __init__(self, claw: Claw):
        self.addRequirements(claw)
        self.claw = claw

        super().__init__(Drop.atLevel4(claw))

    def end(self, interrupted: bool):
        super().end(interrupted)
