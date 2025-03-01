from commands2 import Command

from commands.elevator.moveelevator import MoveElevator
from subsystems.elevator import Elevator


class DiagnoseElevator(Command):
    def __init__(self, elevator: Elevator):
        super().__init__()
        self.addRequirements(elevator)
        self.elevator = elevator

    def initialize(self):
        MoveElevator.toLevel4()

    def isFinished(self) -> bool:
        return True
