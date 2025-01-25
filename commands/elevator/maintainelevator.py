from subsystems.elevator import Elevator
from ultime.command import Command


class MaintainElevator(Command):
    def __init__(self, elevator: Elevator):
        super().__init__()
        self.pivot = elevator
        self.addRequirements(elevator)

    def execute(self):
        if (
            self.pivot.state == Elevator.State.Level1
            or self.pivot.state == Elevator.State.Level2
            or self.pivot.state == Elevator.State.Level3
            or self.pivot.state == Elevator.State.Level4
        ):
            self.pivot.maintain()
        else:
            self.pivot.stop()

    def end(self, interrupted: bool):
        self.pivot.stop()
