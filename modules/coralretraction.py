from commands.claw.retractcoral import RetractCoral
from subsystems.claw import Claw
from subsystems.elevator import Elevator
from ultime.module import Module


class CoralRetractionModule(Module):
    def __init__(self, elevator: Elevator, claw: Claw):
        super().__init__()
        self.elevator = elevator
        self.claw = claw
        self.cmd = RetractCoral(self.claw)

    def robotPeriodic(self) -> None:
        if (
            self.elevator.state == Elevator.State.Level4
            and self.claw.has_coral
            and not self.claw.is_coral_retracted
        ):
            self.cmd.schedule()
