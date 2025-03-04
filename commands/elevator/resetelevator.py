from subsystems.elevator import Elevator
from ultime.command import Command, with_timeout


@with_timeout(10.0)
class ResetElevator(Command):
    def __init__(self, elevator: Elevator):
        super().__init__()
        self.elevator = elevator
        self.addRequirements(elevator)
        self.switch_down_was_pressed = False

    def initialize(self):
        self.switch_down_was_pressed = False
        self.elevator.state = self.elevator.State.Moving

    def execute(self):
        if self.elevator.isDown():  # If the down switch is pressed move up.
            self.elevator.moveUp()
            self.switch_down_was_pressed = True
        else:
            self.elevator.moveDown()  # if switch is not pressed move down until pressed.

    def isFinished(self) -> bool:
        return not self.elevator.isDown() and self.switch_down_was_pressed

    def end(self, interrupted: bool):
        if interrupted:
            self.elevator.state = self.elevator.State.Unknown
            self.elevator.loading_state = self.elevator.LoadingState.Unknown
        else:
            self.elevator.state = self.elevator.State.Reset
            self.elevator.loading_state = self.elevator.LoadingState.FreeToMove
        self.elevator.stop()
