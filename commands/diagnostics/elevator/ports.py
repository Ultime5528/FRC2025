import wpilib
from commands2 import Command

from subsystems.elevator import Elevator
from ultime.autoproperty import autoproperty


class DiagnosePorts(Command):
    time_window = autoproperty(1.0)

    def __init__(self, elevator: Elevator):
        super().__init__()
        self.addRequirements(elevator)
        self.elevator = elevator
        self.timer = wpilib.Timer()

    def initialize(self):
        self.timer.restart()
        self.first_current = self.elevator.getCurrentDrawAmps()

        self.elevator._switch_port_error.set(False)
        self.elevator._motor_port_error.set(False)

    def execute(self):
        self.elevator.moveUp()

    def isFinished(self) -> bool:
        return self.timer.get() <= self.time_window

    def end(self, interrupted: bool):
        if self.elevator.getCurrentDrawAmps() <= self.first_current:
            self.elevator.alert_motor_port_error.set(True)
        self.elevator.stop()
