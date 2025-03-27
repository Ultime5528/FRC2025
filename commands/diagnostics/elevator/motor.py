import wpilib
from commands2 import SequentialCommandGroup, FunctionalCommand, WaitCommand
from commands2.cmd import runOnce, parallel, sequence
from wpilib import DataLogManager, PowerDistribution

import ports
from commands.elevator.moveelevator import MoveElevator
from commands.elevator.resetelevator import ResetElevator
from subsystems.elevator import Elevator
from ultime.autoproperty import autoproperty
from ultime.command import ignore_requirements
from ultime.proxy import proxy


@ignore_requirements(["elevator"])
class DiagnoseMotor(SequentialCommandGroup):
    def __init__(self, elevator: Elevator, pdp: PowerDistribution):
        super().__init__(
            WaitCommand(0.5),
            runOnce(proxy(self.before_command)),
            parallel(
                MoveElevator.toLevel1(elevator),
                sequence(
                    WaitCommand(0.1),
                    FunctionalCommand(
                        lambda: None,
                        proxy(self.while_moving),
                        lambda _: None,
                        proxy(self.has_finished_moving),
                    ),
                ),
            ),
            WaitCommand(0.5),
            runOnce(proxy(self.after_moving)),
            ResetElevator(elevator),
        )
        self.elevator = elevator
        self.pdp = pdp

    def before_command(self):
        self.max_value = 0.0

        if self.pdp.getCurrent(ports.PDP.elevator_motor) > 0.1:
            DataLogManager.log(
                f"Elevator diagnostics: Motor current measured too high. {self.pdp.getCurrent(ports.PDP.elevator_motor)}"
            )
            self.elevator.alert_motor_hi.set(True)

    def while_moving(self):
        self.max_value = max(
            self.max_value, self.pdp.getCurrent(ports.PDP.elevator_motor)
        )

    def has_finished_moving(self):
        return self.elevator.state == Elevator.State.Level1

    def after_moving(self):
        self.elevator.stop()
        if self.pdp.getCurrent(ports.PDP.elevator_motor) > 0.1:
            DataLogManager.log(
                f"Elevator diagnostics: Motor current measured too high. {self.pdp.getCurrent(ports.PDP.elevator_motor)}"
            )
            self.elevator.alert_motor_hi.set(True)

        if self.max_value < 0.1:
            DataLogManager.log(
                f"Elevator diagnostics: Motor current measured too low. {self.max_value}"
            )
            self.elevator.alert_motor_lo.set(True)
