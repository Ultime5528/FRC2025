from commands2 import Command

from subsystems.elevator import Elevator


class DiagnoseElevator(Command):
    def __init__(self, elevator: Elevator):
        super().__init__()
        self.addRequirements(elevator)
        self.elevator = elevator

    def initialize(self):
        if self.elevator.isDown():
            self.elevator._alert_is_down_failed.set(True)

    def isFinished(self) -> bool:
        return True
