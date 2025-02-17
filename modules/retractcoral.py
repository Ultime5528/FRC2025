from commands.claw.backcoral import BackCoral
from subsystems.claw import Claw
from subsystems.elevator import Elevator
from ultime.module import Module


class RetractCoralModule(Module):
    def __init__(self, elevator: Elevator, claw: Claw):
        super().__init__()
        self.elevator = elevator
        self.claw = claw

    def robotPeriodic(self) -> None:
        if (
            self.elevator.state == Elevator.State.Level4
            and self.claw.hasCoralInLoader()
            and not self.claw.isCoralRetracted()
        ):
            cmd = BackCoral(self.claw)
            cmd.schedule()
