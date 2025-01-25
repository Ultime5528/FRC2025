from subsystems.elevator import Elevator
from ultime.command import Command


class ResetElevatorDown(Command):
    def __init__(self, elevator: Elevator):
        super().__init__()
        self.elevator = elevator
        self.addRequirements(elevator)
        self.switch_down_was_pressed = False

    def initialize(self):
        self.switch_down_was_pressed = False

    def execute(self):
        if self.elevator.isDown():  # If the down switch is pressed move up.
            self.elevator.moveUp()
            self.switch_down_was_pressed = True
        else:
            self.elevator.moveDown()  # if switch is not pressed move down until pressed.

    def isFinished(self) -> bool:
        return not self.elevator.isDown() and self.switch_down_was_pressed

    def end(self, interrupted: bool):
        self.elevator.stop()
