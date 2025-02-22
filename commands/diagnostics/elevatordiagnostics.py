import wpilib
from commands2 import Command
from wpilib import PowerDistribution

import ports
from subsystems.elevator import Elevator
from ultime.alert import AlertType
from ultime.autoproperty import autoproperty


class DiagnoseElevator(Command):
    time_window = autoproperty(0.25)

    def __init__(self, elevator: Elevator, pdp: PowerDistribution):
        super().__init__()
        self.addRequirements(elevator)
        self.elevator = elevator
        self.pdp = pdp
        self.timer = wpilib.Timer()
        self.elevator_current = ports.PDP.current_elevator_motor

        self._switch_port_error = self.elevator.createAlert(
            "DIO elevator switch cable is disconnected. Please check connections",
            AlertType.Error,
        )
        self._motor_port_error = self.elevator.createAlert(
            "CAN elevator motor cable is disconnected. Please check connections",
            AlertType.Error,
        )

    def initialize(self):
        self.timer.restart()
        self.first_current = self.pdp.getCurrent(self.elevator_current)
        self._switch_port_error.set(False)
        self._motor_port_error.set(False)

    def execute(self):
        if self.timer.get() <= (self.time_window) / 2:
            self.elevator.moveUp()
        elif self.timer.get() >= (self.time_window) / 2:
            self.elevator.moveDown()

    def isFinished(self) -> bool:
        return self.timer.get() >= self.time_window

    def end(self, interrupted: bool):
        if self.pdp.getCurrent(self.elevator_current) <= self.first_current:
            self._motor_port_error.set(True)
        if not self.elevator._switch.isPressed():
            self._switch_port_error.set(True)
        self.elevator.stop()
