from subsystems.elevator import Elevator
from ultime.command import Command


class MaintainElevator(Command):
    def __init__(self, elevator: Elevator):
        super().__init__()
        self.elevator = elevator
        self.addRequirements(elevator)
        self.should_maintain = False

    def initialize(self):
        self.should_maintain = self.elevator.shouldMaintain()

    def execute(self):
        if self.should_maintain:
            self.elevator.maintain()
        else:
            self.elevator.stop()

    def end(self, interrupted: bool):
        self.elevator.stop()
