from commands2 import Command
import wpilib

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

    def execute(self):
        if self.timer.get() <= self.time_window / 2:
            self.elevator.moveUp()
        elif self.timer.get() >= self.time_window / 2:
            self.elevator.moveDown()

    def isFinished(self) -> bool:
        return self.timer.get() <= self.time_window

    def end(self, interrupted: bool):
        if self.elevator.getCurrentDrawAmps() <= self.first_current:
            self.elevator.alert_motor_port_error.set(True)
        if not self.elevator.isDown():
            self.elevator.alert_switch_port_error.set(True)
        self.elevator.stop()
