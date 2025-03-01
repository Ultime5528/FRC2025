from commands2 import Command

from subsystems.elevator import Elevator
from commands.elevator.moveelevator import MoveElevator
from ultime.alert import AlertType
from ultime.autoproperty import autoproperty


class DiagnoseElevator(Command):
    def __init__(self, elevator: Elevator):
        super().__init__()
        self.addRequirements(elevator)
        self.elevator = elevator

    def initialize(self):


    def execute(self):


    def isFinished(self) -> bool:


    def end(self, interrupted: bool):
