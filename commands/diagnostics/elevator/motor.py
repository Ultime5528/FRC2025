import wpilib
from commands2 import SequentialCommandGroup, FunctionalCommand, WaitCommand
from commands2.cmd import runOnce, parallel, sequence
from wpilib import DataLogManager

from commands.elevator.moveelevator import MoveElevator
from commands.elevator.resetelevator import ResetElevator
from subsystems.elevator import Elevator
from ultime.autoproperty import autoproperty
from ultime.command import ignore_requirements
from ultime.proxy import proxy


@ignore_requirements(["elevator"])
class DiagnoseMotor(SequentialCommandGroup):
    voltage_change_threshold = autoproperty(0.5)

    def __init__(self, elevator: Elevator):
        super().__init__(
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
            ResetElevator(elevator),
        )
        self.elevator = elevator
        self.voltage_before = None
        self.voltage_during = None
        self.voltage_after = None

    def before_command(self):
        self.voltage_before = wpilib.RobotController.getBatteryVoltage()

    def while_moving(self):
        self.voltage_during = wpilib.RobotController.getBatteryVoltage()

    def has_finished_moving(self):
        return self.elevator.state == Elevator.State.Level1

    def end(self, interrupted: bool):
        super().end(interrupted)
        self.elevator.stop()
        self.voltage_after = wpilib.RobotController.getBatteryVoltage()
        voltage_delta_before = self.voltage_before - self.voltage_during
        voltage_delta_after = self.voltage_during - self.voltage_after
        DataLogManager.log(
            "Elevator diagnostics: voltage delta before" + str(voltage_delta_before)
        )
        DataLogManager.log(
            "Elevator diagnostics: voltage delta after" + str(voltage_delta_after)
        )
        if (
            voltage_delta_before < self.voltage_change_threshold
            or voltage_delta_after < self.voltage_change_threshold
        ):
            self.elevator.alert_motor.set(True)
