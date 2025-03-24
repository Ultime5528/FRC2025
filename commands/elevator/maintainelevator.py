from subsystems.elevator import Elevator
from ultime.command import Command


class MaintainElevator(Command):
    def __init__(self, elevator: Elevator):
        super().__init__()
        self.elevator = elevator
        self.addRequirements(elevator)
        self.should_maintain = False
        self._height = 0.0

    def initialize(self):
        self.should_maintain = self.elevator.shouldMaintain()
        self._height = self.elevator.getHeight()

    def execute(self):
        if self.should_maintain and self.elevator.getHeight() < self._height:
            self.elevator.maintain()
        else:
            self.elevator.stop()

    def end(self, interrupted: bool):
        self.elevator.stop()
